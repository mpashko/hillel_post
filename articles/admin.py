import csv

from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from djrichtextfield.widgets import RichTextWidget

from .models import Article, Comment, Section, SuspiciousComment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RichTextWidget}
    }
    list_display = ('article_id', 'title', 'author', 'published')
    list_editable = ('title',)
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="articles.csv"'
        writer = csv.writer(response)
        header = ['Title', 'Author', 'Email', 'Published', 'Comments']
        writer.writerow(header)
        for article in queryset:
            row = [
                article.title,
                article.author.get_full_name(),
                article.author.email,
                article.published,
                article.comments.count()
            ]
            writer.writerow(row)
        return response

    export.short_description = 'Export articles'


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
