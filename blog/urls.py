from django.urls import path, re_path

from . import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index'),
    path(
        'page/<int:page>',
        views.Index.as_view(),
        name='index_page'),
    path(
        'article/<int:id>',
        views.ArticleDetailView.as_view(),
        name='article_detail'),
    path(
        'article/<int:article_id>/edit',
        views.manage_article,
        name='article_edit'),
    path(
        'article/create',
        views.manage_article,
        name='article_create',
        kwargs={'article_id': None}),
    path(
        'category/<str:name>',
        views.CategoryDetailView.as_view(),
        name='category_detail')
    ]
