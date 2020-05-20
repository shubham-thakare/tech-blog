from django.contrib import admin
from apps.website.models.article import Article
from django.utils import timezone


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'last_updated']
    ordering = ['status']

    def make_draft(modeladmin, request, queryset):
        queryset.update(status='d', last_updated=timezone.now())
    make_draft.short_description = "Draft selected articles"

    def make_published(modeladmin, request, queryset):
        queryset.update(status='p', last_updated=timezone.now())
    make_published.short_description = "Publish selected articles"

    def make_withdrawn(modeladmin, request, queryset):
        queryset.update(status='w', last_updated=timezone.now())
    make_withdrawn.short_description = "Withdraw selected articles"

    actions = [make_draft, make_published, make_withdrawn]


admin.site.register(Article, ArticleAdmin)
