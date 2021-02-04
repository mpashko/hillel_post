from django.conf import settings
from django.db import models
from django.utils import timezone


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    articles = models.ManyToManyField(Article, blank=True)
