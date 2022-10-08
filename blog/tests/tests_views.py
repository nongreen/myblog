from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.http.response import HttpResponseRedirect

from accounts.models import BlogUser
from blog.models import Article, Category


class ArticleListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = BlogUser(
            username="tester",
            password="safffaa324s.",
            is_author=True
        )
        self.user.save()
        self.category = Category(name="Test category")
        self.category.save()

        for i in range(10):
            article = Article(
                author=self.user,
                title=f"Article {i}",
                body="Random body",
                category=self.category,
                status="p"
            )
            article.save()

        article = Article(
            author=self.user,
            title="Article drafted",
            body="Random body",
            category=self.category,
            status="d"
        )
        article.save()

        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0")

    def test_get_request(self):
        response = self.client.get(reverse("index"))
        self.assertTrue(isinstance(response, HttpResponseRedirect))

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(reverse(
            "article_list",
            kwargs={"page": 2}
        ))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_pagination(self):
        response = self.client.get(reverse(
            "category_detail",
            kwargs={
                "category_id": self.category.id,
                "page": 1
            })
        )
        article_list_queryset = response.context[0]["article_list"]

        self.assertTrue(0 < len(article_list_queryset) <= settings.PAGINATE_BY)

    def test_draft_function(self):
        response = self.client.get(reverse(
            "category_detail",
            kwargs={
                "category_id": self.category.id,
                "page": 1
            })
        )
        article_list_queryset = response.context[0]["article_list"]
        article = Article.objects.get(title="Article drafted")

        self.assertFalse(article in article_list_queryset)


class ArticleDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.user = BlogUser(
            username="tester",
            password="safffaa324s.",
            is_author=True
        )
        self.user.save()

        self.category = Category(name="Test category")
        self.category.save()

        self.article = Article(
            author=self.user,
            title="Article",
            body="Random body",
            category=self.category,
            status="p"
        )
        self.article.save()

        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0")

    def test_get_request(self):
        response = self.client.get(reverse(
            "article_detail",
            kwargs={"article_id": self.article.id}
        ))
        self.assertTrue(self.article.title in str(response.content))


class CategoryDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.user = BlogUser(
            username="tester",
            password="safffaa324s.",
            is_author=True
        )
        self.user.save()

        self.category = Category(name="Test category")
        self.category.save()

        for i in range(10):
            article = Article(
                author=self.user,
                title=f"Article {i}",
                body="Random body",
                category=self.category,
                status="p"
            )
            article.save()

        article = Article(
            author=self.user,
            title="Article drafted",
            body="Random body",
            category=self.category,
            status="d"
        )
        article.save()

        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0")

    def test_get_request(self):
        response = self.client.get(reverse(
            "category_detail",
            kwargs={
                "category_id": self.category.id,
                "page": 1
            })
        )

        # Test response
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_pagination(self):
        response = self.client.get(reverse(
            "category_detail",
            kwargs={
                "category_id": self.category.id,
                "page": 1
            })
        )
        article_list_queryset = response.context[0]["article_list"]

        self.assertTrue(0 < len(article_list_queryset) <= settings.PAGINATE_BY)

    def test_draft_function(self):
        response = self.client.get(reverse(
            "category_detail",
            kwargs={
                "category_id": self.category.id,
                "page": 1
            })
        )
        article_list_queryset = response.context[0]["article_list"]
        article = Article.objects.get(title="Article drafted")

        self.assertFalse(article in article_list_queryset)


class ArticleManagementViewTest(TestCase):
    def setUp(self) -> None:
        self.category = Category(name="category")
        self.category.save()

        self.user = BlogUser(
            username="tester",
            password="safffaa324s.",
            is_author=True
        )
        self.user.save()

        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0")

    def test_get_request_creation(self):
        response = self.client.get(
            reverse("article_create")
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_request_modification(self):
        response = self.client.get(
            reverse("article_create")
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_invalid_post_request_creation(self):
        response = self.client.post(
            reverse("article_create"),
            data={
                "title": None,
                "body": 3
            }
        )
