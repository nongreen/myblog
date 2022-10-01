from django.forms import ModelForm
from .models import Article
from mdeditor.widgets import MDEditorWidget


class ArticleForm(ModelForm):
    """ Uses for creation and edition articles. """

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = MDEditorWidget(attrs={'rows': 30})

    class Meta:
        model = Article
        fields = ['title', 'body', 'category']
