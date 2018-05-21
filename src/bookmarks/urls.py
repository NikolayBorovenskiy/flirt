# coding: utf-8

from django.conf.urls import url

import bookmarks.views


urlpatterns = [
    url(r'^add/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        bookmarks.views.add_bookmark, name='add_bookmark'),
]
