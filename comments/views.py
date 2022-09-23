from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import get_user

from .forms import CommentPostForm
from blog.models import Article
from .models import Comment


# Create your views here.
class CommentPostView(FormView):
    form_class = CommentPostForm
    template_name = "comments/comment_creation_form.html"
    # todo: redirect to a article
    success_url = '/'
    user = None

    def form_valid(self, form):
        if form.is_valid():
            article_id = self.kwargs.get("article_id")
            article = Article.objects.get(pk=article_id)

            comment = form.save(False)

            comment.article = article
            comment.author = self.user

            if parent_comment_id := form.cleaned_data["parent_comment_id"]:
                parent_comment = Comment.objects.get(pk=parent_comment_id)
                comment.parent_comment = parent_comment

            form.instanace = comment

            form.save()

            # return super(CommentPostView, self).form_valid(form)
            return HttpResponseRedirect(f"/article/{article_id}")

        else:
            return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        self.user = get_user(request)

        return super(CommentPostView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user = get_user(request)

        return super(CommentPostView, self).get(request, *args, **kwargs)
