from django.conf import settings
from django.db import models
from django.utils import timezone


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def author_email(self):
        return self.author.email

    def to_dict(self):
        return {
            'title': self.title,
            'author_email': self.author_email
        }


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    articles = models.ManyToManyField(Article, blank=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.article}'

    @property
    def article_author_email(self):
        return self.article.author_email

    def to_dict(self):
        return {
            'article': self.article.to_dict(),
            'name': self.name,
            'email': self.email,
            'text': self.text
        }


class SuspiciousComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment.text
