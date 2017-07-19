from django.conf.urls import url

from . import views

app_name = 'upvote'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^un/(?P<slug>[\w\-]+)$', views.DetailView.as_view(), name='detail'),
    url(r'^un/(?P<slug>[\w\-]+)/vote/$', views.vote, name='vote'),
    url(r'^ajax/vote/$', views.ajax_vote, name='ajax_vote'),
]