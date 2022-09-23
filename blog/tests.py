from django.test import TestCase
from django.test import Client, RequestFactory

from accounts.models import BlogUser
from blog.models import Article, Category


# Create your tests here.
class ArticleTest(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.get_or_create(
            email='tester@test.com',
            username='tester',
            password='tsettseT1',
            is_author=True
        )[0]
        self.user.save()

        self.category = Category.objects.get_or_create(name='test_category')[0]
        self.category.save()

    def test_validate_article(self):
        article = Article()
        article.author = self.user
        article.title = "test"
        article.body = "test est test test test test test"
        article.category = self.category
        article.slug = "test"
        article.save()

