# todo: add tests
# todo: add cache
# todo: add to admin permissions to editing and viewing any articles
import logging

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import Article, Category
from .forms import ArticleForm
from comments.forms import CommentPostForm

logger = logging.getLogger(__name__)


# Create your views here.
class Index(ListView):
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'

    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        return article_list


class ArticleDetailView(DetailView):
    template_name = "blog/article_detail.html"
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'id'
    user = None

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object(queryset)
        obj.viewed(self.user)
        return obj

    def get(self, request, *args, **kwargs):
        self.user = get_user(request)

        return super(ArticleDetailView, self).get(request)

    def get_context_data(self, **kwargs):
        comment_form = CommentPostForm()

        kwargs['form'] = comment_form
        kwargs['article_comments'] = self.object.article_comments()

        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryDetailView(ListView):
    template_name = "blog/category_detail.html"
    model = Category
    context_object_name = 'article_list'

    def get_queryset(self):
        queryset_name = self.kwargs["name"]
        category = get_object_or_404(Category, name=queryset_name)

        article_list = Article.objects.filter(
            category=category
            )

        return article_list


def manage_article(request, article_id=None):
    if article_id:
        article = Article.objects.get(id=article_id)

        if request.method == "GET":
            form = ArticleForm(instance=article)
            return render(
                request,
                'blog/article_edition_form.html',
                {'form': form}
            )
        if request.method in ("POST", "PUT"):
            form = ArticleForm(request.POST, instance=article)
            if request.POST.get("del"):
                # todo: getting article from link (kwargs)
                article = form.save(False)
                article.delete()

                return HttpResponseRedirect('/')
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/article/{article_id}')
            else:
                return render(
                    request,
                    'blog/article_edition_form.html',
                    {'form': form}
                )
    else:
        article = Article()

        if request.method == "GET":
            form = ArticleForm(instance=article)
            return render(
                request,
                'blog/article_edition_form.html',
                {'form': form}
            )
        if request.method in ("POST", "PUT"):
            form = ArticleForm(request.POST, instance=article)

            if form.is_valid():
                article = form.save(False)
                user = get_user(request)
                article.author = user

                form.instance = article
                form.save()

                article = form.save(False)
                article_id = article.id

                return HttpResponseRedirect(f'/article/{article_id}')

            else:
                return render(
                    request,
                    'blog/article_edition_form.html',
                    {'form': form}
                )
