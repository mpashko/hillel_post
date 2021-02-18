from django import forms

from .models import Article, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text')
