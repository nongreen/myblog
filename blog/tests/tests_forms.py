import logging

from django.test import TestCase

from accounts.models import BlogUser
from blog.forms import ArticleManagementForm
from blog.models import Article, Category


class ArticleManagementFormTest(TestCase):
    def setUp(self) -> None:
        self.form = ArticleManagementForm()

    def test_form_save(self):
        user = BlogUser(
            username="tester",
            password="randomPassword12",
            is_author=True
        )
        user.save()
        category = Category(name="category")
        category.save()

        form = ArticleManagementForm(
            data={
                "title": "Simple title",
                "body": "Some big body ...",
                "category": str(category.id)
            })
        article = form.save(False)
        article.author = user
        form.instance = article

        if form.is_valid():
            form.save()
        else:
            logging.error(form.errors)

        self.assertTrue(
            Article.objects.get(title="Simple title")
        )

    def test_form_fields(self):
        # Test fields
        form_fields = list(self.form.fields.keys())
        map_result = list(map(
            lambda is_in: is_in in form_fields,
            ["title", "body", "category"]
        ))
        self.assertFalse(
            False in map_result
        )

        # Test count fields
        if len(map_result) < len(form_fields):
            logging.warning("Fields added to form without update tests")
