# todo: add cache
from django.shortcuts import render
from django.views.generic import ListView

from .models import Post


# Create your views here.
class Index(ListView):
    template_name = 'blog/index.html'
    # model = Post

    def get_queryset_data(self):
        post_list = Post.objects.all()
        return post_list

    def get_queryset(self):
        post_list = self.get_queryset_data()
        return post_list
