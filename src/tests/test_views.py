# coding: utf-8

import pytest

from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_home(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert response.templates[0].name == 'home.html'


def test_robots_txt(client):
    response = client.get(reverse('robots_txt'))
    assert response.status_code == 200
    assert response.templates[0].name == 'robots.txt'
    assert response['Content-Type'] == 'text/plain'
