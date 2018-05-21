from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from accounts.models import DatingUser
from bookmarks.models import Bookmark
from core import context


@login_required
def add_bookmark(request, email):
    context_dict = {}
    if request.method == 'POST':
        instance = get_object_or_404(DatingUser, email=email)
        with context.acquire(request.user):
            if instance:
                Bookmark.objects.create(
                    owner=context.get_user(),
                    marked_user_id=instance.id
                )
                context_dict['user'] = dict(
                    pk=instance.pk,
                    last_name=instance.last_name,
                    first_name=instance.first_name,
            )

    return JsonResponse(context_dict)