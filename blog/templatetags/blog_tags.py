from django import template
from django.urls.base import reverse


register = template.Library()


@register.inclusion_tag('blog/tags/post_pagination.html')
def load_pagination_info(page_obj):
    next_url = ''
    previous_url = ''

    if page_obj.has_next():
        next_number = page_obj.next_page_number()
        next_url = reverse('index_page', kwargs={'page': next_number})
    if page_obj.has_previous():
        previous_number = page_obj.previous_page_number()
        previous_url = reverse('index_page', kwargs={'page': previous_number})

    return {
        'next_url': next_url,
        'previous_url': previous_url,
        'page_obj': page_obj
    }


@register.inclusion_tag('blog/tags/article_info.html')
def load_article_info(article):
    return {'article': article}


@register.inclusion_tag('blog/tags/sidebar.html')
def load_sidebar(user):
    return {}


# todo: add reverse
@register.simple_tag
def get_profile_url(user):
    site = '127.0.0.1:8000'
    username = user.username

    url = f"http://{site}/profile/{username}"

    return url

@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)


@register.simple_tag
def test(user):
    return user.__class__
