from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from articles.models import Article, Comment


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
        cls.article = Article(title=cls.title, text=cls.text, author=cls.user)

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
        self.article.full_clean()

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
        expected_email = self.user.email
        self.assertEqual(self.article.author_email, expected_email)

    def test_to_dict_equals_to_short_representation(self):
        # expected = {'title': self.title, 'author_email': self.user.email}
        expected = {'title': self.title, 'author_email': self.article.author_email}
        self.assertEqual(self.article.to_dict(), expected)

    def test_validate_article_representation(self):
        expected_repr = self.title
        self.assertEqual(self.article.__str__(), expected_repr)


class CommentModelTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@gmail.com'
        )
        self.article = Article(
            title='some title',
            text='some text',
            author=user
        )
        self.comment = Comment(
            article=self.article,
            name='some name',
            email='some@email.com',
            text='some text'
        )

    def test_validate_to_dict_method(self):
        expected_resp = {
            'name': self.comment.name,
            'email': self.comment.email,
            'text': self.comment.text,
            'article': {
                'title': self.article.title,
                'author_email': self.article.author_email
            }
        }
        self.assertEqual(self.comment.to_dict(), expected_resp)
