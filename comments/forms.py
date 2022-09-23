from django import forms
from django.forms import ModelForm
from django.forms import widgets

from .models import Comment


class CommentPostForm(ModelForm):
    parent_comment_id = forms.IntegerField(
        widget=widgets.HiddenInput, required=False
    )

    class Meta:
        model = Comment
        fields = ['body']
