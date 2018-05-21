import uuid

from django.db import models
from django.utils.timezone import now

from accounts.models import DatingUser
from core.utils import ChoiceEnum


class Thread(models.Model):
    identity_field = 'uuid'

    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    members = models.ManyToManyField(DatingUser)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

    @property
    def last_message(self):
        if hasattr(self, '_last_message'):
            return self._last_message
        last_message = self.message_set.all().last()
        self._last_message = last_message
        return last_message

    def __str__(self):
        return ', '.join(user.get_full_name() for user in self.members.all())


class Message(models.Model):
    identity_field = 'uuid'

    class Type(ChoiceEnum):
        Content = 'content'
        NewMember = 'new-member'
        MemberLeft = 'member-left'

    uuid = models.UUIDField(default=uuid.uuid4)
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(DatingUser)
    content = models.CharField(max_length=500, null=True)
    type = models.CharField(max_length=20, choices=Type.choices())

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
