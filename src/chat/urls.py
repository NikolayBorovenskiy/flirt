# coding: utf-8

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'notifications/(?P<notification_uuid>[^/.]+)/mark_viewed/$',
        views.mark_viewed, name='marked-view'),
    url(r'thread/$', views.create_private, name='private'),
    url(r'thread/(?P<thread_uuid>[^/.]+)/messages/$', views.messages,
        name='message'),
    url(r'$', views.chat_list, name='list-view'),
]
