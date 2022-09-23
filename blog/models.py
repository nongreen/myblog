from django.db import models
from django.utils import timezone
from myblog.settings import LENGTH_SHORT_BODY

from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    STATUS_CHOICES = (('p', 'Published'), ('d', 'Draft'))

    id = models.BigAutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Author',
        blank=False,
        null=False,
        default=None,
        limit_choices_to={'is_author': True},
        on_delete=models.CASCADE
        )

    category = models.ForeignKey(
        'blog.Category',
        verbose_name='Category',
        blank=True,
        default=None,
        on_delete=models.CASCADE
    )

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

    @property
    def short_body(self):
        return self.body[0:LENGTH_SHORT_BODY]


class Category(models.Model):
    name = models.CharField(
        'name',
        max_length=40,
        null=False,
        unique=False,
        blank=False
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
