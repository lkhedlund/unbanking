from django.conf.urls import url

from . import views

app_name = 'upvote'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<word>[\w\-]+)$', views.DetailView.as_view(), name='detail'),
]