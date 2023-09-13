from typing import Dict, Any

from django.core.cache import cache
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render

from waapuro import urls
from waapuro.publish.models import Article
from waapuro_code.indexer import *


def index_status(request):
    # make indexer
    _index = WaapuroIndexer()

    view_data: Dict[str, Any] = {
        'totality': len(_index.files),
        'indexed': ArticleUrlWcfMapping.objects.all().count(),
        'cached': Article.objects.all().count()
    }

    def _VIEW():
        return render(request, 'index_status.html', {
            "vd": view_data,
            "adminpath": urls.admin_url,
        }, using='waapuro')

    def _APIs():
        # Initialize the result
        _result: Dict[str, Any] = {
            "code": 0,
            "msg": "",
            "data": {},
        }

        # get method params
        method = request.POST.get("method")
        if method is None:
            return HttpResponseBadRequest("The method parameter is not defined.")
        # GET view data
        elif method == "get_data":
            _result["data"] = view_data
            return JsonResponse(_result)

        # START searchWaapuroFiles
        elif method == "action_searchWaapuroFiles":
            _index.search_waapuro_files()
            _result["msg"] = "Searching Waapuro file."
            return JsonResponse(_result)
        # START buildIndex
        elif method == "action_buildIndex":
            _index.build_index()
            _result["msg"] = "Building Index, Please wait for some minuses."
            return JsonResponse(_result)
        # START profileCollection
        elif method == "action_profileCollection":
            _index.collect_profiles()
            _result["msg"] = "Collecting, Please wait for some minuses."
            return JsonResponse(_result)

        # START Flow
        elif method == "action_startFlow":
            _index.flow_build_index()
            _result["msg"] = "Starting Flow, Please wait for some minuses."
            return JsonResponse(_result)
        else:
            return HttpResponseBadRequest("This method is not found.")

    if request.method == 'GET':
        return _VIEW()
    elif request.method == 'POST':
        return _APIs()
    else:
        return HttpResponseNotAllowed("Not Allowed.")
