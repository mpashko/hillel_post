from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Article


class ArticleListViewTest(TestCase):

    NUMBER_OF_ARTICLES = 10

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

    def test_lists_all_articles(self):
        resp = self.client.get(reverse('get_articles'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['articles']) == self.NUMBER_OF_ARTICLES)
