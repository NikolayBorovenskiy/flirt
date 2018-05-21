from logging import warn

# from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

empty = serializers.empty


class Context:

    def __init__(self, user, data_query):
        self.user = user or None
        # self.user = user or AnonymousUser()
        self.data_query = data_query


__global_context = None


def acquire(user=None, data_query=empty):
    global __global_context
    if __global_context is not None:
        warn("Context already acquired")
    #     raise Exception("Context already acquired")
    __global_context = Context(user, data_query)
    return _Autorelease()


def is_acquired():
    return __global_context is not None


def release():
    global __global_context
    if __global_context is None:
        warn("There is no context to release")
    __global_context = None


def _get_context():
    if __global_context is None:
        warn("Context is not acquired")
        return Context(None, empty)
    return __global_context


def get_user():
    return _get_context().user


def get_data_query():
    return _get_context().data_query


class _Autorelease:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        release()
