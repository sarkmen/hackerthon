from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.idea_new, name='idea_new'),
    url(r'^$', views.idea_list, name="idea_list" ),
    url(r'^(?P<pk>\d+)/$', views.idea_detail, name='idea_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.idea_edit, name='idea_edit'),
    url(r'^(?P<pk>\d+)/del/$', views.idea_del, name='idea_del'),
    url(r'^(?P<idea_pk>\d+)/comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^(?P<idea_pk>\d+)/comment/(?P<pk>\d+)/del/$', views.comment_del, name='comment_del'),
    #Sample
    url(r'^location/$', views.location, name="location")
]
