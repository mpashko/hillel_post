from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import ArticleCreateView, ArticleDeleteView, ArticleEditView

urlpatterns = [
    path('', views.get_articles, name='index'),
    path('articles/', views.get_articles, name='get_articles'),
    path('articles/new', ArticleCreateView.as_view(), name='create_article'),
    # path('articles/', cache_page(60 * 5)(views.get_articles), name='get_articles'),
    path('articles/<int:article_id>/', views.get_article, name='get_article'),
    path('articles/<int:pk>/edit/', ArticleEditView.as_view(), name='edit_article'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete_article'),
    path('articles/<slug:tag_slug>/', views.get_articles, name='get_articles_by_tag')
]
