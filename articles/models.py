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

    def __str__(self):
        return self.title


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    articles = models.ManyToManyField(Article, blank=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    username = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.username} on {self.article}'
