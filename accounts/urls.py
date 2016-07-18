from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': 'index'}, name='logout'),
    #url(r'^signup/$', views.sign_up, name="signup"),
    url(r'^resume/$', views.resume, name="resume"),
]

