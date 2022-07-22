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