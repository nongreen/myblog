# todo: add tests
# todo: add cache
# todo: add to admin permissions to editing and viewing any articles
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Category
from .forms import ArticleForm
from comments.forms import CommentPostForm


# Create your views here.
class ArticleListView(ListView):
    """ It's index page """

    template_name = 'blog/article_list.html'
    model = Article
    context_object_name = 'article_list'
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'


class ArticleDetailView(DetailView):
    template_name = "blog/article_detail.html"
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'id'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = get_user(request)

        obj = self.get_object()
        obj.register_view(self.user)

        return super(ArticleDetailView, self).get(request)

    def get_context_data(self, **kwargs):
        comment_form = CommentPostForm()

        kwargs['form'] = comment_form
        kwargs['comments_to_self_article'] = \
            self.object.comments_to_self_article

        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryDetailView(ListView):
    """ Uses to storage and show articles inhered to same category """
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


def manage_article_view(request, article_id=None):
    # Edition article, if can
    if article_id:
        try:
            article = Article.objects.get(id=article_id)
        except ObjectDoesNotExist:
            return render(
                request,
                'share_layout/error_page.html',
                {'body': 'Article not found'}
            )

        # GET request handler
        if request.method == "GET":
            form = ArticleForm(instance=article)
            return render(
                request,
                'blog/article_edition_form.html',
                {'form': form}
            )

        # POST and PUT requests handler
        if request.method in ("POST", "PUT"):
            form = ArticleForm(request.POST, instance=article)

            if request.POST.get("del"):
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
    # Creation article
    else:
        article = Article()

        # GET requests handler
        if request.method == "GET":
            form = ArticleForm(instance=article)
            return render(
                request,
                'blog/article_edition_form.html',
                {'form': form}
            )

        # POST and PUT requests handler
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
