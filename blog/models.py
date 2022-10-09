import logging
import ast

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from django.db import models
from django.utils import timezone
from myblog.settings import LENGTH_SHORT_BODY
from mdeditor.fields import MDTextField

from accounts.models import BlogUser

logger = logging.getLogger(__name__)


class Article(models.Model):
    """
    Author, title, body, category are required. Other are optional
    Important! Don't update status directly. Use set_status
    """

    STATUS_CHOICES = (('p', 'Published'), ('d', 'Draft'))

    id = models.BigAutoField(primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="author",
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
        blank=False,
        null=False,
        default=None,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    body = MDTextField('Body', null=False, blank=False)

    publish = models.DateTimeField(default=timezone.now, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(default=timezone.now, editable=False)

    # Important! Don't update status directly. Use set_status
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='d',
        editable=False
    )

    viewed_users = models.ManyToManyField(
        BlogUser,
        related_name="viewed_users"
    )

    class Meta:
        ordering = ['-publish']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        if update_fields and not (
            "viewed_users_list" in update_fields and
            len(update_fields) == 1
        ):
            self.updated = timezone.now()

        super(Article, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def set_status(self, new_status: str) -> None:
        """ Realize autoupdate publish time """
        if self.status == new_status:
            return

        if new_status == 'p':
            self.status = new_status
            self.publish = timezone.now()
        elif new_status == 'd':
            self.status = new_status
        else:
            raise ValueError(
                "new_status must be 'p' or 'd'. Got a {0}".format(new_status)
            )

        self.save()

    def register_view(self, user: BlogUser or AnonymousUser) -> None:
        """ Add present user to viewed_user, if he isn't in it"""
        self_article = Article.objects.get(id=self.id)

        if isinstance(user, BlogUser) and \
                user.username not in self_article.viewed_users.all():
            self_article.viewed_users.add(user)
            self_article.save()
        elif isinstance(user, BlogUser) and user.username in self.viewed_users:
            return
        elif isinstance(user, AnonymousUser):
            return
        else:
            raise ValueError(f"Required BlogUser, excepted {type(user)}")

    @property
    def views_count(self):
        return self.viewed_users.all().count()

    @property
    def comments_to_self_article(self) -> QuerySet:
        comments = self.comment_set.filter(is_enable=True)
        return comments

    @property
    def short_body(self):
        return self.body[0:LENGTH_SHORT_BODY]


# todo: create validator for name (one of parameters is dont start with spaces)
class Category(models.Model):
    """ Storage articles. Name required. """
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        'name',
        max_length=40,
        null=False,
        unique=True,
        blank=False,
        default=None
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
