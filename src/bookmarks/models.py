from django.db import models

from accounts.models import DatingUser


# Create your models here.
class Bookmark(models.Model):
    owner = models.ForeignKey(DatingUser)
    marked_user_id = models.IntegerField(
        verbose_name=u'Отмеченный пользователь')
    date_created = models.DateTimeField(
        u'Дата создания', auto_now_add=True, auto_now=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.owner.email

    def __unicode__(self):  # __unicode__ on Python 2
        return self.owner.email
