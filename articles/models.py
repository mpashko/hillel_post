from django.conf import settings
from django.db import models
from django.utils import timezone
import os, sys


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    articles = models.ManyToManyField(Article, blank=True)



class someUglyClass(models.Model):
    """Extra long docstring --------------------------------------------------------"""
    text = models.TextField()

    def Method_A(self):
        pass
        # return os.environ.get('a')

    def method_b(self):
        pass
        # return sys.argv