from django.forms import ModelForm, BaseModelFormSet
from .models import Article
from mdeditor.widgets import MDEditorWidget


class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = MDEditorWidget(attrs={'rows': 30})

    class Meta:
        model = Article
        fields = ['title', 'body', 'category', 'status']
