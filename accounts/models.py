# todo: add permissions by groups

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.urls import reverse


# Create your models here.
class BlogUser(AbstractUser):
    """ Username and password required. Other fields are optional"""
    username = models.SlugField(
        'Username',
        max_length=30,
        blank=False,
        default=None,
        unique=True
    )
    password = models.CharField(
        'Password',
        max_length=100,
        blank=False,
        default=None
    )
    nickname = models.CharField(
        'Nickname',
        max_length=150,
        blank=False,
        unique=False,
        default=username
    )
    email = models.EmailField('Email', blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'username'

    created_time = models.DateTimeField(
        'Created time',
        default=now,
        editable=False
    )
    last_mod_time = models.DateTimeField('Last mod time', default=now)

    is_moderator = models.BooleanField('Is moderator', default=False)
    is_author = models.BooleanField('Is author', default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = "User"
        verbose_name_plural = "Users"
        get_latest_by = "id"

    def __str__(self):
        return self.username

    def get_profile_url(self) -> str:
        profile_path = reverse('accounts:profile',
                               kwargs={'username': self.username})
        return profile_path
