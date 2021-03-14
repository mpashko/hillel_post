from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.get_articles),
    path('articles/', views.get_articles, name='get_articles'),
    # path('articles/', cache_page(60 * 5)(views.get_articles), name='get_articles'),
    path('articles/<int:article_id>/', views.get_article, name='get_article'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article')
]
