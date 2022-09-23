from django.urls import path

from comments.views import CommentPostView

app_name = 'comments'
urlpatterns = [
    path(
        'article/<int:article_id>/postcomment',
        CommentPostView.as_view(),
        name='comment_post'
         )
]