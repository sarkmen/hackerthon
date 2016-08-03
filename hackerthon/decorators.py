from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import Http404
from accounts.models import Resume

def user_wrote_this(model):
    def _my_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            try:
                model_instance = get_object_or_404(model, pk= kwargs['pk'])
            except Http404:
                messages.error(request, "잘못된 접근입니다.")
                return redirect('projects:index')
            if model_instance.author != request.user:
                messages.error(request, '작성자만 접근 가능합니다.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return view_func(request,*args,**kwargs)
        return _decorator
    return _my_decorator

def get_resume():
    def _my_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            try:
                model_instance = get_object_or_404(Resume, user=request.user)
            except Http404:
                messages.error(request, "해커톤 참석을 위해 참가지원서를 작성하셔야 합니다.")
                return redirect('accounts:resume')
            return view_func(request, *args, **kwargs)
        return _decorator
    return _my_decorator