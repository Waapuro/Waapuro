from django.http import HttpResponseNotFound, Http404

from functools import wraps


def superuser_required(view_func):
    """
    Decorator to restrict view access to superusers only.
    Returns HTTP 404 if the user is not a superuser.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404()
        return view_func(request, *args, **kwargs)

    return _wrapped_view
