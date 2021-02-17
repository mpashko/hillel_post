from django.contrib import admin

from .models import Article, Section, Comment, SuspiciousComment

admin.site.register(Article)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(SuspiciousComment)
