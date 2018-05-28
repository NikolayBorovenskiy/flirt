# coding: utf-8
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.forms import UserChangeForm
from bookmarks.models import Bookmark
from core.serializers import user as serialize_user
from .models import DatingUser


def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(
                reverse('accounts:profile', kwargs={'slug': 'self'}))
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'account/edit.html', args)


def profile(request, slug=None):
    context = {}
    if slug == 'self':
        instance = get_object_or_404(DatingUser, email=request.user)
        bookmarks = map(
            lambda obj: get_object_or_404(DatingUser, pk=obj.marked_user_id),
            instance.bookmark_set.all()
        )
        context['instance'] = instance
        context['bookmarks'] = bookmarks
    else:
        instance = get_object_or_404(DatingUser, slug=slug)
        my_bookmarks = Bookmark.objects.filter(
            owner__email=request.user,
            marked_user_id=instance.id
        )
        context['is_bookmark'] = True if my_bookmarks.count() else False
    context['instance'] = instance

    return render(request, 'account/profile.html', context)


def get_user_info(request):
    context_dict = {}
    if request.method == 'GET' and request.user.is_authenticated():
        user = serialize_user(request.user)
        context_dict = user

    return JsonResponse(context_dict)
