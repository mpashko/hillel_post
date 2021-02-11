from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_articles),
    path('articles/', views.get_articles, name='get_articles'),
    path('articles/<int:article_id>/', views.get_article, name='get_article'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article')
]
