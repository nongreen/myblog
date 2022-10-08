from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        '',
        RedirectView.as_view(url='/1'),
        name='index'
    ),
    path(
        '<int:page>',
        views.ArticleListView.as_view(),
        name='article_list'
    ),
    path(
        'article/<int:article_id>',
        views.ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        'article/<int:article_id>/edit',
        views.manage_article_view,
        name='article_edit'
    ),
    path(
        'article/create',
        views.manage_article_view,
        name='article_create',
        kwargs={'article_id': None}
    ),
    path(
        'category/<int:category_id>/<int:page>/',
        views.CategoryDetailView.as_view(),
        name='category_detail'
    )
    ]
