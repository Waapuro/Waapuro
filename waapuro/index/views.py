import functools
import os
import random
from io import BytesIO

from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, Http404

from PIL import Image

from waapuro import settings
from waapuro.publish.models import *
from waapuro.settings import BASE_DIR
from waapuro_code.parser.HTML import WC2HTML


def index(request):
    return render(request, 'index.html')


def article(request, sub_path):
    """
    Articles detail page
    """
    sub_path = f"/{sub_path}"
    all_ = Article.objects.filter()
    matched = None
    for obj in all_:
        if obj.real_url == sub_path:
            matched = obj
    if matched:
        # get waapuro_file path
        waapuro_filepath = ArticleUrlWcfMapping.objects.get(url=matched.url).wc_path

        # TODO:未来将waapuro code读取类整合
        with open(waapuro_filepath, 'r', encoding='utf-8') as file:
            content = WC2HTML(wc_str=file.read()).parse()

            return render(request, "article.html", {
                "article": matched,
                "content": content,
            })
    else:
        raise Http404()


""" Build-in Pages """


def limit_ip_requests(limit, ban=60 * 10):
    """
    DDoS Protector([IP]request/sec)

    Add `@limit_ip_requests(10, 60 * 10)` to top of Views.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            ip_address = request.META.get('REMOTE_ADDR')

            # 从缓存中获取当前IP的访问次数
            requests_count = cache.get(ip_address, 0)

            # 如果超过限制，则返回错误响应
            if requests_count >= limit:
                response = JsonResponse({'error': 'Request limit exceeded'}, status=429)
                return response

            # 如果未超过限制，则增加访问计数并调用视图函数
            cache.set(ip_address, requests_count + 1, ban)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def version(request):
    return render(request, 'waapuro.html', {
        'settings': settings
    }, using='waapuro')


def favicon(request, *args, **kwargs):
    return redirect('/builtin/waapuro', param_name={
        "format": "ico",
        "size": "128"
    })


@limit_ip_requests(20)
def waapuro_logo(request):
    format_type = request.GET.get('format', 'webp')  # Default: webp
    size = int(request.GET.get('size', 512))  # Default: 512
    cache_key = f"waapuroLogo_{format_type}_{size}"

    # get image from cache
    image_data = cache.get(cache_key)
    if image_data:
        return HttpResponse(image_data, content_type=f'image/{format_type}')

    # safety check
    allow_format = ["PNG", "ICO", "WEBP"]
    max_size = 1024
    if not (16 <= size <= max_size and size % 16 == 0) or format_type.upper() not in allow_format:
        return HttpResponseBadRequest(
            f"Allow format `{'`, `'.join(allow_format)}`. Size <= {max_size} and must be integer of 16.")

    # convert
    file_path = os.path.join(BASE_DIR, 'builtin/static/img/waapuro_logo/waapuro.png')
    image = Image.open(file_path)
    image = image.resize((size, size), Image.BICUBIC)
    output = BytesIO()

    image.save(output, format=format_type.upper(), quality=98)
    image_data = output.getvalue()

    # Add data to cache
    cache.set(cache_key, image_data, 60 * random.randint(6, 12))

    return HttpResponse(image_data, content_type=f'image/{format_type}')
