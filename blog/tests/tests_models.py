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

    def test_permissions(self):
        no_author = BlogUser.objects.get_or_create(
            email='no_author@test.com',
            username='no_author',
            password='1122qqWW'
        )[0]
        author = BlogUser.objects.get_or_create(
            email='author@test.com',
            username='author',
            password='1122qqWW',
            is_author=True
        )[0]
        some_author = BlogUser.objects.get_or_create(
            email='some_author@test.com',
            username='some_author',
            password='1122qqWW',
            is_author=True
        )

        # Test of trying to create article by no author
        article = Article()
        article.author = no_author
        article.title = 'test permission'
        article.body = 'test'
        self.assertRaises(PermissionError, article.save)

        # Test of trying to create article by author
        article.author = author
        article.save()

    def test_validate_article(self):
        article = Article()
        article.author = self.user
        article.title = "test"
        article.body = "test est test test test test test"
        article.category = self.category
        article.slug = "test"
        article.save()

