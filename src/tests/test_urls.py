# coding: utf-8

import pytest

from django.core.urlresolvers import reverse, resolve


def test_home():
    match = resolve('/')
    assert match.view_name == 'home'
    assert match.url_name == 'home'
    assert not match.app_name
    assert not match.namespace

    assert reverse('home') == '/'


def test_robots_text():
    match = resolve('/robots.txt')
    assert match.view_name == 'robots_txt'
    assert match.url_name == 'robots_txt'
    assert not match.app_name
    assert not match.namespace

    assert reverse('robots_txt') == '/robots.txt'
