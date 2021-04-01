import pytest
from django.test import TestCase

from articles.forms import ArticleForm


class ArticleFormTest(TestCase):

    def test_expected_fields(self):
        form = ArticleForm()
        expected_fields = {'title', 'text'}
        self.assertEqual(set(form.fields.keys()), expected_fields)

    def test_title_validation_failure(self):
        form_data = {'title': 'a' * 101, 'text': 'some text'}
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())


# def test_article_form_validation():
#     form_data = {'title': 'some title', 'text': 'some text'}
#     form = ArticleForm(data=form_data)
#     assert form.is_valid() is True
#
#
# def test_title_validation_failure():
#     form_data = {'title': 'a' * 101, 'text': 'some text'}
#     form = ArticleForm(data=form_data)
#     assert form.is_valid() is False


@pytest.mark.parametrize('form_data, expected_result', [
    pytest.param({'title': 'some title', 'text': 'some text'}, True),
    pytest.param({'title': 'a' * 101, 'text': 'some text'}, False)
])
def test_article_form_validation(form_data, expected_result):
    form = ArticleForm(data=form_data)
    assert form.is_valid() is expected_result
