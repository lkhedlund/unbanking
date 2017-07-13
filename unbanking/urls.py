from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^loomonauts/', admin.site.urls),
    url(r'^', include('upvote.urls')),
]
