import redis
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

# from core import api, context, mail
from core import context
import json
from core.serializers import serialize_model
from . import conf
from .models import Notification, NotificationDelivery
from .registry import get_notification_type_info, register_notification_type

_redis_publish = redis.StrictRedis(
    host=conf.MESSAGING_REDIS_HOST,
    port=conf.MESSAGING_REDIS_PORT,
).publish

register_notification_type("new-message", inform_admins=False, with_actor=False)
register_notification_type("message-edited", inform_admins=False,
                           with_actor=False)
register_notification_type("message-deleted", inform_admins=False,
                           with_actor=False)


def deliver_message(message, serialized_message):
    if serialized_message.get('deleted'):
        typename = "message-deleted"
    elif message.created == message.thread.updated:
        typename = "new-message"
    else:
        typename = "message-edited"
    content = {
        'thread': message.thread.uuid,
        'message': serialized_message,
        'received_time': message.updated,
    }
    send_notification(
        typename=typename,
        receivers=message.thread.members.all(),
        content=content,
    )


def send_notification(typename, receivers, content):
    type_info = get_notification_type_info(typename)
    receivers = map(_get_user, receivers)
    if context.is_acquired() and type_info.with_actor:
        user = context.get_user()
        if user.is_authenticated():
            content['actor'] = user
    if type_info.send_push:
        content_str = json.dumps({
            key: serialize_model(val)
            for key, val in content.items()
        })
        notification = Notification.objects.create(
            type=typename, content=content_str)
        NotificationDelivery.objects.bulk_create([
            NotificationDelivery(receiver=user, notification=notification)
            for user in receivers
        ])
        _redis_publish(conf.MESSAGING_REDIS_CHANNEL, json.dumps({
            'type': 'notification',
            'data': {
                'id': notification.id,
                'typename': typename
            }
        }))


def _get_notification_delivery(notification_uuid):
    delivery = get_object_or_404(
        NotificationDelivery, notification__uuid=notification_uuid,
        receiver=context.get_user()
    )
    return delivery


def mark_as_viewed(notification_uuid):
    delivery = _get_notification_delivery(notification_uuid)
    if delivery.viewed_datetime is None:
        delivery.viewed_datetime = now()
        delivery.save(update_fields=['viewed_datetime'])


def _get_user(obj):
    # if isinstance(obj, (PatientProfile, DoctorProfile)):
    #     obj = obj.user
    return obj
