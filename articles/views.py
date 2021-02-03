from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Article


def get_articles(request):
    articles = Article.objects.all().order_by('-published')
    return render(request, 'articles/get_articles.html', {'articles': articles})

