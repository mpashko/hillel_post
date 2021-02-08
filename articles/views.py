from django.shortcuts import get_object_or_404, render

from .forms import CommentForm
from .models import Article


def get_articles(request):
    articles = Article.objects.all().order_by('-published')
    print(articles)
    return render(request, 'articles/get_articles.html', {'articles': articles})


def get_article(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article_id = article.article_id
            new_comment.save()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': CommentForm(),
        'new_comment': new_comment
    }

    return render(request, 'articles/get_article.html', context)
