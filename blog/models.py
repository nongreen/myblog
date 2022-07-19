from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


LENGHT_SHORT_BODY = 70


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=100, unique_for_date='publish')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
            max_length=10, 
            choices=STATUS_CHOICES, 
            default='d' 
            )

    def __str__(self):
        return self.title

    # todo: get_short_body as property
    def get_short_body(self):
        return self.body[0:LENGHT_SHORT_BODY]
