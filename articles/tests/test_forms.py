from django.test import TestCase

from articles.forms import ArticleForm


class ArticleFormTest(TestCase):

    def test_expected_fields(self):
        form = ArticleForm()
        expected_fields = {'title', 'text'}
        self.assertEquals(set(form.fields.keys()), expected_fields)

    def test_title_validation_failure(self):
        form_data = {'title': 'a' * 101, 'text': 'some text'}
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
