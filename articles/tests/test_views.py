from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Article
from articles.tests.factory import UserFactory
from exchanger.models import ExchangeRate


class ArticleListViewTest(TestCase):

    NUMBER_OF_ARTICLES = 10

    _EXPECTED_RATES = [
        ExchangeRate(
            currency_a='USD',
            currency_b='UAH',
            buy=25.99,
            sell=26.12
        ),
        ExchangeRate(
            currency_a='EUR',
            currency_b='UAH',
            buy=25.99,
            sell=26.12
        ),
        ExchangeRate(
            currency_a='RUB',
            currency_b='UAH',
            buy=25.99,
            sell=26.12
        )
    ]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(first_name='John', last_name='Doe')
        for article_num in range(cls.NUMBER_OF_ARTICLES):
            Article.objects.create(
                title=f'Article #{str(article_num)}',
                text='some text',
                author=user
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/articles/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('get_articles'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('get_articles'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'articles/get_articles.html')

    @patch('articles.views.get_exchange_rates')
    def test_lists_all_articles(self, mock_request):
        mock_request.return_value = self._EXPECTED_RATES
        resp = self.client.get(reverse('get_articles'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['articles']) == self.NUMBER_OF_ARTICLES)

    @patch('articles.views.get_exchange_rates')
    def test_validate_exchange_rate_table(self, mock_request):
        mock_request.return_value = self._EXPECTED_RATES
        resp = self.client.get(reverse('get_articles'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['xrates']), 6)


@pytest.mark.django_db
def test_article_creation():
    user = User.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@gmail.com'
    )
    Article.objects.create(title='some title', text='some text', author=user)
    assert Article.objects.count() == 1


@pytest.mark.django_db
def test_view_articles_url_exists_at_desired_location(client):
    resp = client.get('/articles/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get('/admin/articles/article/')
    assert response.status_code == 302
    assert '/admin/login/' in response.url


@pytest.mark.django_db
def test_superuser_view(admin_client):
    response = admin_client.get('/admin/articles/article/')
    assert response.status_code == 200


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(first_name='John', last_name='Doe')


@pytest.fixture
def article(user):
    return Article.objects.create(title='Article', text='some text', author=user)


@pytest.fixture
def create_articles(django_user_model, user):
    def make_articles(**kwargs):
        author = kwargs['author'] if 'author' in kwargs else user
        number_of_articles = kwargs['number_of_articles']
        articles = []
        for article_num in range(number_of_articles):
            article = Article.objects.create(
                title=f'Article #{str(article_num)}',
                text='some text',
                author=author
            )
            articles.append(article)
        return articles
    return make_articles


@pytest.mark.django_db
def test_lists_all_articles(client, create_articles):
    number_of_articles = 4
    create_articles(number_of_articles=number_of_articles)

    resp = client.get(reverse('get_articles'))
    assert resp.status_code == 200

    articles = resp.context['articles']
    assert len(articles) == number_of_articles

    article = articles[0]
    assert article.author.first_name == 'John'


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return UserFactory.create(**kwargs)
    return make_user


@pytest.mark.django_db
def test_list_all_articles_created_by_another_user(client, create_user, create_articles):
    author_name = 'Jane'
    user = create_user(first_name=author_name, username='jane_doe')
    number_of_articles = 2
    create_articles(number_of_articles=number_of_articles, author=user)

    resp = client.get(reverse('get_articles'))
    assert resp.status_code == 200

    articles = resp.context['articles']
    assert len(articles) == number_of_articles

    article = articles[0]
    assert article.author.first_name == author_name


@pytest.mark.django_db
def test_hide_edit_button_for_not_authenticated_user(client, create_articles):
    articles = create_articles(number_of_articles=1)
    article = articles[0]
    resp = client.get(reverse('get_article', kwargs={'article_id': article.article_id}))
    assert resp.status_code == 200

    expected_link = f'<a href="/articles/{article.article_id}/edit/">'
    assert expected_link.encode() not in resp.content


@pytest.fixture
def auto_login_user(client, create_user):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.force_login(user)
        return client, user
    return make_auto_login


@pytest.mark.django_db
def test_show_edit_button_for_authenticated_user(client, auto_login_user, create_articles):
    articles = create_articles(number_of_articles=1)
    article = articles[0]

    client, user = auto_login_user()

    resp = client.get(reverse('get_article', kwargs={'article_id': article.article_id}))
    assert resp.status_code == 200

    expected_link = f'<a href="/articles/{article.article_id}/edit/">'
    assert expected_link.encode() in resp.content
