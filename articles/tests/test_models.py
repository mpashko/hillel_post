from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from articles.models import Article


class ArticlesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # вызывается каждый раз перед запуском теста на уровне настройки
        # всего класса
        # print('setUpTestData')
        cls.title = 'some title'
        cls.text = 'some text'
        cls.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@gmail.com'
        )

    def setUp(self) -> None:
        # вызывается перед каждой тестовой функцией для настройки объектов,
        # которые могут изменяться во время тестов
        pass

    def tearDown(self) -> None:
        pass

    # def test_false_is_false(self):
    #     self.assertFalse(False)
    #
    # def test_true_is_false(self):
    #     self.assertTrue(False)

    def test_successful_article_creation(self):
        article = Article(title=self.title, text=self.text, author=self.user)
        article.full_clean()

    def test_failure_due_to_long_title(self):
        long_title = 'a' * 101
        article = Article(title=long_title, text=self.text, author=self.user)
        # with self.assertRaises(ValidationError):
        expected_message = 'Ensure this value has at most 100 characters (it has 101).'
        with self.assertRaisesMessage(ValidationError, expected_message):
            article.full_clean()

    def test_failure_due_to_user_is_none(self):
        article = Article(title=self.title, text=self.text, author=None)
        expected_message = 'This field cannot be null.'
        with self.assertRaisesMessage(ValidationError, expected_message):
            article.full_clean()

    def test_author_email_is_equal_to_user_email(self):
        article = Article(title=self.title, text=self.text, author=self.user)
        expected_email = self.user.email
        self.assertEqual(article.author_email, expected_email)

    def test_to_dict_equals_to_short_representation(self):
        article = Article(title=self.title, text=self.text, author=self.user)
        # expected = {'title': self.title, 'author_email': self.user.email}
        expected = {'title': self.title, 'author_email': article.author_email}
        self.assertEqual(article.to_dict(), expected)
