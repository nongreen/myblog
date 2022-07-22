# todo: add cache
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings

from .models import Post


# Create your views here.
class Index(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_queryset(self):
        post_list = Post.objects.all()
        return post_list


class PostDetailView(DetailView):
    template_name = "blog/post_detail.html"
    model = Post
    context_object_name = 'post'
    slug_url_kwarg = "slug"
