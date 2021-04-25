import jwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler
from taggit.models import Tag

from exchanger.models import ExchangeRate
from exchanger.tasks import get_exchange_rates
from hillel_post.settings import ARTICLES_PER_PAGE, SECRET_KEY
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from .serializers import ArticleSerializer


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


class ArticleEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    template_name = 'articles/edit_article.html'
    fields = ['title', 'text', 'cover', 'tags']
    permission_required = ['is_staff']


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('index')


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'title': rdata.get('title'),
            'text': rdata.get('text'),
            'author': request.user.pk,
        }
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'DELETE':
        article.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        title = request.data.get('title')
        if title:
            article.title = title
        text = request.data.get('text')
        if text:
            article.text = text
        article.save()
        return Response(status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        res = {'error': 'Please provide an email and a password'}
        return Response(res)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        message = "Can't find user with the specified email"
        res = {'error': message}
        return Response(res, status=HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        message = "Can't authenticate with the given credentials or the account has " \
                  "been deactivated"
        res = {'error': message}
        return Response(res, status=HTTP_403_FORBIDDEN)

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, SECRET_KEY)
    user_details = {
        'user_id': user.pk,
        'name': f'{user.first_name} {user.last_name}',
        'token': token
    }
    return Response(user_details, status=HTTP_200_OK)
