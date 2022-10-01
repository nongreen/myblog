# todo: add tests
# todo: add cache
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from myblog.settings import ERROR_MESSAGES
from myblog.utils import error_page
from .models import Article, Category
from .forms import ArticleForm
from comments.forms import CommentPostForm


class ArticleListView(ListView):
    """ It's index page. Queryset restricted to only published. """

    template_name = 'blog/article_list.html'
    model = Article
    context_object_name = 'article_list'
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_queryset(self):
        article_list = super(ArticleListView, self).get_queryset()
        article_list = article_list.filter(status="p")
        return article_list


class ArticleDetailView(DetailView):
    """ View of detail article. Also uses to view comments to article """
    template_name = "blog/article_detail.html"
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
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
        return edition_article(request, article_id)
    # Creation article
    else:
        return creation_article(request)


def article_form(request, article):
    form = ArticleForm(instance=article)
    return render(
        request,
        'blog/article_form.html',
        {'form': form}
    )


def creation_article(request):
    article = Article()

    # GET requests handler
    if request.method == "GET":
        return article_form(request, article)

    # POST and PUT requests handler
    if request.method in ("POST", "PUT"):
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            article = form.save(False)
            user = get_user(request)

            if user.is_author:
                article.author = user
            else:
                raise PermissionError("User isn't author")

            form.instance = article
            form.save()

            article = form.save(False)
            article_id = article.id

            return HttpResponseRedirect(reverse(
                "article_detail",
                kwargs={"article_id": article_id}
            ))

        else:
            return render(
                request,
                'blog/article_form.html',
                {'form': form}

            )


def edition_article(request, article_id):
    # Trying to get article
    try:
        article = Article.objects.get(id=article_id)
    except ObjectDoesNotExist:
        return error_page(
            request,
            ERROR_MESSAGES["Edit nonexistent article"]
        )

    # GET request handler
    if request.method == "GET":
        return article_form(request, article)

    # POST and PUT requests handler
    if request.method in ("POST", "PUT"):
        # Checks of user on permissions.
        user = get_user(request)
        if user != article.author or not (user.is_superuser
                                          or user.is_moderator):
            return error_page(request, ERROR_MESSAGES["Permission denied"])

        form = ArticleForm(request.POST, instance=article)

        # Delete article, if it needs
        if request.POST.get("delete"):
            article = form.save(False)
            article.delete()

            return HttpResponseRedirect('/')

        if form.is_valid():
            if new_status := request.POST.get("publish" or "draft"):
                article.set_status(new_status)

            form.save()

            return HttpResponseRedirect(f'/article/{article_id}')
        else:
            return render(
                request,
                'blog/article_form.html',
                {
                    'form': form,
                    'author': article.author
                }
            )
