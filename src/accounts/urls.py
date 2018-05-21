# coding: utf-8

from django.conf.urls import url

from accounts import views


urlpatterns = [
    url(r'edit/$', views.edit_profile, name='edit'),
    url(r'user/self/$', views.get_user_info, name='user-info'),
    url(r'^(?P<slug>[\w-]+)$', views.profile, name='profile'),
]
