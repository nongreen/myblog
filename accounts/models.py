from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# Create your models here.
class BlogUser(AbstractUser):
    username = models.CharField(
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

    created_time = models.DateTimeField('Created time', default=now)
    last_mod_time = models.DateTimeField('Last mod time', default=now)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']
        verbose_name = "User"
        verbose_name_plural = "Users"
        get_latest_by = "id"
