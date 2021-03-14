from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from exchanger.models import ExchangeRate
from .forms import ArticleForm, CommentForm
from .models import Article, Comment


# @cache_page(60 * 5)
def get_articles(request):
    articles = Article.objects.all().order_by('-published')
    exchange_rates = ExchangeRate.objects.all()
    context = {
        k: v for ex_rate in exchange_rates
        for k, v in ex_rate.to_dict().items()
    }

    # context = {}
    # for ex_rate in exchange_rates:
    #     for k, v in ex_rate.to_dict.item():
    #         context[k] = v

    context['articles'] = articles
    return render(request, 'articles/get_articles.html', context)


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
        'new_comment': new_comment and Comment.objects.get(id=new_comment.id)
    }

    return render(request, 'articles/get_article.html', context)


def edit_article(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published = timezone.now()
            article.save()
            return redirect('get_article', article_id=article_id)

    form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form})
