from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from django.utils import timezone
from django.test import TestCase

from accounts.models import BlogUser
from blog.models import Article, Category


# Create your tests here.
class ArticleTest(TestCase):
    def setUp(self):
        self.user = self._create_user("tester")
        self.category = Category.objects.get_or_create(name='test_category')[0]
        self.category.save()

    def test_permissions(self):
        """ No actual """
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

        # Test of trying to create article by no author
        article = Article()
        article.author = no_author
        article.title = 'test permission'
        article.body = 'test'
        article.category = self.category

        # Test of trying to create article by author
        article.author = author
        article.save()

    def test_creation_article(self):
        article = Article()
        article.author = self.user
        article.title = "test"
        article.body = "test est test test test test test"
        article.category = self.category
        article.save()

        with self.assertRaises(IntegrityError):
            article = Article()
            article.save()

    def test_modification_article(self):
        article = self._create_article()

        # Test mutable property of article
        article.title = "tests"
        article.save()

        # Test autoupdate updated time
        start_time = timezone.now()
        article_updated_time = article.updated
        end_time = timezone.now()

        self.assertFalse(start_time < article_updated_time < end_time)

    def test_setter_status(self):
        article = self._create_article()

        # Test autoupdate of publish time
        start_time = timezone.now()
        article.set_status('p')
        article.save()
        article_publish_time = article.publish
        end_time = timezone.now()
        self.assertTrue(start_time < article_publish_time < end_time)

        start_time = timezone.now()
        article.set_status('d')
        article.save()
        article_publish_time = article.publish
        end_time = timezone.now()

        self.assertFalse(start_time < article_publish_time < end_time)

    def test_register_view(self):
        second_user = self._create_user("second")
        article = self._create_article()

        article.register_view(self.user)

        # Test arguments handler
        with self.assertRaises(ValueError):
            article.register_view("not user")

        article = self._create_article(author=second_user)

        # Test saving by register_view
        start_state_of_list = article.viewed_users.all().count()
        article.register_view(self.user)
        end_state_of_list = article.viewed_users.all().count()
        self.assertNotEqual(start_state_of_list, end_state_of_list)

        start_state_of_list = article.viewed_users.all().count()
        article.register_view(self.user)
        end_state_of_list = article.viewed_users.all().count()
        self.assertEqual(start_state_of_list, end_state_of_list)

        # Test register AnonymousUser
        anonymous_user = AnonymousUser()
        article.register_view(anonymous_user)

    def test_views_count(self):
        article = self._create_article()
        self.assertTrue(isinstance(article.views_count, int))

        # Test viewed_users count
        article.viewed_users.add(self.user)
        article.save()
        self.assertEqual(article.views_count, 1)

    def _create_article(
            self,
            author: BlogUser = None,
            category: Category = None
    ):
        article = Article(
            author=author or self.user,
            title="test",
            body="test est test test test test test",
            category=category or self.category
        )
        article.save()
        return article

    def _create_user(self, username):
        user = BlogUser.objects.get_or_create(
            email=f'{username}@test.com',
            username=f'{username}',
            password='tsettseT1',
            is_author=True
        )[0]
        return user


class CategoryTest(TestCase):
    def test_category_creation(self):
        category = Category()
        category.name = "Test name"
        category.save()

        with self.assertRaises(IntegrityError):
            category = Category()
            category.save()
