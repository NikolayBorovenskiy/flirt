# coding: utf-8
import datetime
import operator
from functools import reduce

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.shortcuts import render

from accounts.models import DatingUser
from core import context


def home(request):
    context_dict = {
        'title': u'Участники'
    }
    with context.acquire(request.user):
        queryset_list = DatingUser.objects.all()
        user = context.get_user()
        context_dict['object_list'] = queryset_list
        context_dict['user_bookmarks_ids'] = []
        if user.is_authenticated():
            user_bookmarks = user._wrapped.bookmark_set.all()
            user_bookmarks_ids = [bookmark.marked_user_id for bookmark in user_bookmarks]
            context_dict['user_bookmarks_ids'] = user_bookmarks_ids

    return render(request, "home.html", context_dict)


def robots_txt(request):
    return render(
        request, 'robots.txt', {}, content_type='text/plain')


def members_list(request):
    search_query = request.GET.get('search')
    gender_query = request.GET.getlist('gender[]')
    age_query = request.GET.getlist('age[]')
    qs = list()
    if search_query:
        qs = DatingUser.objects.filter(
            Q(last_name__contains=search_query) |
            Q(first_name__contains=search_query) |
            Q(job__icontains=search_query) |
            Q(university__icontains=search_query) |
            Q(country__icontains=search_query)
        ).distinct()
    if gender_query:
        _qs = qs or DatingUser.objects
        and_statements = [Q(**{'gender': q}) for q in gender_query]
        qs = _qs.filter(reduce(operator.or_, and_statements))
    if age_query:
        _qs = qs or DatingUser.objects
        start = datetime.date.today() - relativedelta(years=int(age_query[1]))
        end = datetime.date.today() - relativedelta(years=int(age_query[0]))
        qs = _qs.filter(date_of_birth__range=[start, end])

    if not search_query and not gender_query and not age_query:
        qs = DatingUser.objects.all()

    return render(request, 'members.html', {'instances': qs})