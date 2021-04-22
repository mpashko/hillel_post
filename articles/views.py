from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from taggit.models import Tag

from exchanger.models import ExchangeRate
from exchanger.tasks import get_exchange_rates
from hillel_post.settings import ARTICLES_PER_PAGE
from .forms import ArticleForm, CommentForm
from .models import Article, Comment


# @cache_page(60 * 5)
def get_articles(request, tag_slug=None):
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = Article.objects.filter(tags__in=[tag]).order_by('-published')
    else:
        articles = Article.objects.all().order_by('-published')

    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    exchange_rates = ExchangeRate.objects.all()
    xrates = {
        # k: v for ex_rate in get_exchange_rates()
        k: v for ex_rate in exchange_rates
        for k, v in ex_rate.to_dict().items()
    }

    # context = {}
    # for ex_rate in exchange_rates:
    #     for k, v in ex_rate.to_dict.item():
    #         context[k] = v

    context = {'xrates': xrates}
    context['articles'] = articles
    context['page'] = page
    context['edited'] = request.session.get('edited')
    context['tags'] = Tag.objects.all().order_by('name')
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


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published = timezone.now()
            article.save()

            edited = request.session.get('edited')
            if edited:
                request.session['edited'].append(article_id)
            else:
                request.session['edited'] = [article_id]
            request.session.modified = True

            return redirect('get_article', article_id=article_id)

    form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/create_article.html'
    fields = ['title', 'text', 'cover', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'articles/edit_article.html'
    fields = ['title', 'text', 'cover', 'tags']


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('index')
