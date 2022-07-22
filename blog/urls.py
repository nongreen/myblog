from django.urls import path

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
        'post/<int:slug>',
        views.PostDetailView.as_view(),
        name='detail')
    ]
