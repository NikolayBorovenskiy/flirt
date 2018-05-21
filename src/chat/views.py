from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from accounts.models import DatingUser
from chat.implementation import read_list_of_messages, read_list_of_threads, \
    send_message, start_private
from core import context
from core.serializers import thread as thread_serializer, \
    user as user_serializer
from notifications_service import api as notifications_service_api
from .models import Thread


def chat_list(request):
    context_dict = dict()
    with context.acquire(request.user):
        context_dict['threads'] = read_list_of_threads()

    return render(request, "chat/chat_list.html", context_dict)


@login_required
def create_private(request):
    context_dict = {}
    if request.method == 'POST':
        email_field = request.POST.get('email')
        if email_field:
            target_user = get_object_or_404(DatingUser, email=email_field)
            with context.acquire(request.user):
                thread = start_private(target_user)
                context_dict['created'] = thread.created
                context_dict['last_message'] = thread.last_message
                context_dict['updated'] = thread.updated
                context_dict['uuid'] = thread.uuid
                context_dict['members'] = [
                    dict(id=member.id,
                         email=member.email,
                         last_name=member.last_name,
                         first_name=member.first_name,
                         avatar=member.avatar.url
                         ) for member in thread.members.all()]
    return JsonResponse(context_dict)


@login_required
def messages(request, thread_uuid):
    context_dict = {}
    target_thread = get_object_or_404(Thread, uuid=thread_uuid)
    if request.method == 'POST':
        content_field = request.POST.get('content')
        if content_field:
            with context.acquire(request.user):
                message = send_message(target_thread, content_field)
                context_dict['uuid'] = message.uuid
                context_dict['content'] = message.content
                context_dict['created'] = str(message.created)
                context_dict['updated'] = str(message.updated)
                context_dict['type'] = message.type
                context_dict['author'] = user_serializer(message.author)
                context_dict['thread'] = thread_serializer(message.thread)

        return JsonResponse(context_dict)
    elif request.method == 'GET':
        with context.acquire(request.user):
            context_dict['messages'] = read_list_of_messages(target_thread)

        return render(request, "chat/messages_list.html", context_dict)


@login_required
def mark_viewed(request, notification_uuid):
    context_dict = {}
    if request.method == 'POST':
        with context.acquire(request.user):
            notifications_service_api.mark_as_viewed(notification_uuid)
    return JsonResponse(context_dict)
