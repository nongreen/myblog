# todo: add cache
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings

from .models import Article


# Create your views here.
class Index(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_queryset(self):
        post_list = Article.objects.all()
        return post_list


class ArticleDetailView(DetailView):
    template_name = "blog/article_detail.html"
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = "slug"
