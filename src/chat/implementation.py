from django.db.models import Count

from core import context
from core.exceptions import ValidationError
from core.serializers import serialize_model
from notifications_service import api as notifications_service_api
from notifications_service.api import register_notification_type
from .models import Message, Thread


# ---------------------------- THREAD ---------------------------------
def read_list_of_threads():
    return Thread.objects.filter(members=context.get_user()).order_by(
        '-updated')


def read_list_of_messages(thread):
    return Message.objects.filter(thread=thread).order_by('created')


def start_private(target_user):
    user = context.get_user()
    if target_user == user:
        raise ValidationError("You cannot start a chat with yourself")

    # try to find existing thread between these two users
    thread = (
        Thread.objects
            .annotate(Count('members'))
            .filter(members__count=2)
            .filter(members=target_user)
            .filter(members=user)
            .first()
    )
    # create a thread if it does not exist
    if not thread:
        thread = Thread.objects.create()
        thread.members.add(target_user, user)
        notifications_service_api.send_notification(
            typename='started-chat',
            receivers=[target_user],
            content={'thread': thread}
        )

    return thread


register_notification_type(
    'started-chat', inform_admins=False
)


# ---------------------------- MESSAGE ---------------------------------
def send_message(thread, content):
    user = context.get_user()
    message = Message.objects.create(
        content=content,
        author=user,
        type=Message.Type.Content,
        thread=thread,
    )
    _update_thread(thread, message.created)
    _deliver(message)
    return message


def _deliver(message):
    notifications_service_api.deliver_message(message, serialize_model(message))


def _update_thread(thread, time):
    thread.updated = time
    thread.save(update_fields=['updated'])
