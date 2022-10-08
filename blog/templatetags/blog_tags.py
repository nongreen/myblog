from django import template
from django.urls.base import reverse
from markdown import markdown

register = template.Library()


@register.inclusion_tag('blog/tags/article_pagination.html')
def load_pagination_info(page_obj):
    next_url = ''
    previous_url = ''

    if page_obj.has_next():
        next_number = page_obj.next_page_number()
        next_url = reverse('article_list', kwargs={'page': next_number})
    if page_obj.has_previous():
        previous_number = page_obj.previous_page_number()
        previous_url = reverse('article_list', kwargs={'page': previous_number})

    return {
        'next_url': next_url,
        'previous_url': previous_url,
        'page_obj': page_obj
    }


@register.inclusion_tag('blog/tags/article_info.html')
def load_article_info(article):
    return {'article': article}


@register.simple_tag
def get_profile_url(user):
    username = user.username

    url = reverse("accounts:profile", kwargs={"username": username})

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
def get_html_from_markdown(markdown_text) -> str:
    return markdown(markdown_text)


@register.simple_tag
def test(user):
    return user.__class__
