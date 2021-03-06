from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from idea import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^idea/', include('idea.urls', namespace='idea')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
