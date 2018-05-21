import enum
import uuid

from django.db import models

from accounts.models import DatingUser


class _ContentFieldType(enum.IntEnum):
    Raw = 1
    Model = 2
    ModelWithBody = 3

    def __str__(self):
        return str(self.value)


class Notification(models.Model):
    identity_field = 'uuid'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(max_length=50)
    content = models.CharField(max_length=2000)
    receivers = models.ManyToManyField(DatingUser,
                                       through='NotificationDelivery')
    created = models.DateTimeField(auto_now_add=True)


class NotificationDelivery(models.Model):
    identity_field = None

    class Meta:
        unique_together = ['receiver', 'notification']

    receiver = models.ForeignKey(DatingUser)
    notification = models.ForeignKey('Notification')
    sent = models.BooleanField(default=False)
    viewed_datetime = models.DateTimeField(null=True)

    @property
    def viewed(self):
        return self.viewed_datetime is not None
