from django.shortcuts import render
from django.contrib.sites.models import Site

from hashlib import sha256


def error_page(request, body):
    """ Return response as error_page """
    return render(
        request,
        'share_layout/error_page.html',
        {"body": body}
    )


# todo: rename decoded_str
def get_sha256(decoded_str):
    encoded_str = sha256(decoded_str.encode('utf-8'))
    return encoded_str.hexdigest()


def get_current_site():
    site = Site.objects.get_current()
    return site
