from django.contrib import admin

from .models import Article, Section, Comment

admin.site.register(Article)
admin.site.register(Section)
admin.site.register(Comment)
