from functools import wraps

from django.shortcuts import HttpResponse

def ajax_required(func):
    @wraps(func)
    def inner(request,*args, **kwargs):
        if request.is_ajax():
            return func(request)
        return HttpResponse('不是ajax发送的请求')
    return inner

