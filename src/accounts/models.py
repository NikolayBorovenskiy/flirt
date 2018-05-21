# coding: utf-8

from ckeditor.fields import RichTextField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models
from django.db.models.signals import pre_save
from django_countries.fields import CountryField

from core.utils import pre_save_slug_post_receiver


class DatingUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class DatingUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('m', u'Мужской'),
        ('f', u'Женский'),
        ('o', u'Другой'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    last_name = models.CharField(verbose_name=u'Фамилия', max_length=20)
    first_name = models.CharField(verbose_name=u'Имя', max_length=20)
    gender = models.CharField(verbose_name=u'Пол',
                              max_length=1,
                              choices=GENDER_CHOICES)
    date_of_birth = models.DateField(verbose_name=u'День рождения',
                                     help_text=u'2000-04-11',
                                     null=True,
                                     blank=True)
    avatar = models.ImageField(verbose_name=u'Аватар',
                               upload_to='avatars/',
                               null=True,
                               blank=True)
    university = models.CharField(
        verbose_name=u'Место учебы',
        null=True,
        blank=True,
        max_length=100
    )
    job = models.CharField(verbose_name=u'Место работы',
                           max_length=100,
                           null=True,
                           blank=True, )
    country = CountryField(blank_label=u'(Выберите страну)')
    twitter = models.CharField(verbose_name='Twitter',
                               max_length=200,
                               validators=[URLValidator()],
                               null=True,
                               blank=True)
    facebook = models.CharField(verbose_name='Facebook',
                                max_length=200,
                                null=True,
                                blank=True,
                                validators=[URLValidator()])
    instagram = models.CharField(verbose_name='Instagram',
                                 max_length=200,
                                 validators=[URLValidator()],
                                 null=True,
                                 blank=True)
    bio = RichTextField(verbose_name=u'О себе', null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name=u'Присоеденился',
                                       auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(editable=False, unique=True, null=True, blank=True)

    objects = DatingUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"slug": self.slug})

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


pre_save.connect(pre_save_slug_post_receiver, sender=DatingUser)
