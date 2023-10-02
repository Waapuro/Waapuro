from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# paginate
def paginate_queryset(queryset, page_number, items_per_page):
    """
    articles = Article.objects.all().order_by('-publish_date')  # 查询集

    page_number = request.GET.get('page')
    items_per_page = 10  # 每页显示的项数

    paginated_articles = paginate_queryset(articles, page_number, items_per_page)
    """
    paginator = Paginator(queryset, items_per_page)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    next_page_number = page.next_page_number() if page.has_next() else None
    total_pages = paginator.num_pages

    return {
        "items": list(page),
        "next": next_page_number,
        "total": total_pages
    }
