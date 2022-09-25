from django.db import models
from mdeditor.fields import MDTextField

from accounts.models import BlogUser
from blog.models import Article


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(
        BlogUser,
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        verbose_name='Article',
        on_delete=models.CASCADE
    )
    parent_comment = models.ForeignKey(
        'self',
        verbose_name='Parent',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    is_enable = models.BooleanField(
        'is_enable',
        default=True,
        blank=False,
        null=False
    )
    body = models.TextField('Body')

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = verbose_name
        ordering = ['id']
        get_latest_by = 'id'

    @property
    def death(self):
        """
        Return _death summed with 1 (for display in template)
        """

        return self._death + 1

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        if self.parent_comment:
            self._death = self.parent_comment.death
        else:
            self._death = 0

    def __str__(self):
        return self.body
