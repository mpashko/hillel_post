from django.shortcuts import render

from .models import Article


def get_articles(request):
    articles = Article.objects.all().order_by('-published')
    return render(request, 'articles/get_articles.html', {'articles':
                                                              articles})

