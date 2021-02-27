from django.contrib import admin
from django.db import models
from djrichtextfield.widgets import RichTextWidget

from .models import Article, Comment, Section, SuspiciousComment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RichTextWidget}
    }
    list_display = ('article_id', 'title', 'author', 'published')
    list_editable = ('title',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    # filter_horizontal = ('articles',)
    filter_vertical = ('articles',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'active')
    actions = ['make_inactive']
    actions_selection_counter = False

    def make_inactive(self, request, queryset):
        queryset.update(active=False)

    make_inactive.short_description = 'Mark inactive'


admin.site.register(SuspiciousComment)
