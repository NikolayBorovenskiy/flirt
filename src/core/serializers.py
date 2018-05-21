import json

from accounts.models import DatingUser
from chat.models import Message, Thread
from core.exceptions import ModelSerializerDoesNotDefine
from notifications_service.models import Notification


def thread(model):
    result = {
        "uuid": str(model.uuid),
        "members": list(map(lambda x: user(x), model.members.all())),
        "last_message": message(
            model.last_message) if model.last_message else model.last_message,
        "created": str(model.created),
        "updated": str(model.updated)
    }

    return result


def message(model):
    result = {
        "uuid": str(model.uuid),
        "type": model.type,
        "content": model.content,
        "author": user(model.author),
        "created": str(model.created),
        "updated": str(model.updated)
    }

    return result


def notification(model):
    result = {
        "_datetime": model.created,
        "_type": model.type,
        "_uuid": model.uuid,
    }
    result.update(json.loads(model.content))

    return result


def user(model):
    result = {
        "id": model.id,
        "email": model.email,
        "last_name": model.last_name,
        "first_name": model.first_name,
        "avatar": model.avatar.url
    }
    return result


_MODEL_SERIALIZERS = {
    Thread: thread,
    DatingUser: user,
    Notification: notification,
    Message: message
}


def _get_serializer(model):
    try:
        serializer = _MODEL_SERIALIZERS[type(model)]
    except IndexError as ex:
        msg = 'No serializer for model {}'.format(model)
        raise ModelSerializerDoesNotDefine(msg) from ex

    return serializer


def serialize_model(model):
    if hasattr(model, '_wrapped'):
        model = model._wrapped
    serializer = _MODEL_SERIALIZERS.get(type(model))
    if serializer:
        result = serializer(model)
    else:
        if isinstance(model, dict):
            result = model
        else:
            result = str(model)

    return result
