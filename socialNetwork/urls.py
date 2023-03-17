from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, reverse_lazy, re_path
from django.views.static import serve


def empty(*args, **kwargs):
    return HttpResponse('')


urlpatterns = [
    path('empty_page', empty, name='empty_page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('feed.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
