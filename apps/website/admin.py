from django.contrib import admin
from apps.website.models.article import Article
from django.utils import timezone
from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from apps.website.helpers.utils import get_article_read_time_from_file, \
    get_article_read_time_from_html, \
    get_article_dir_path, get_article_file_name, \
    remove_file, read_article_html_text


class ArticleAdminForm(forms.ModelForm):
    content = RichTextUploadingFormField(required=False)

    class Meta:
        model = Article
        fields = ['title', 'keywords', 'description', 'public_image', 'status']


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ['title', 'status', 'last_updated']
    ordering = ['status']
    search_fields = ('id', 'title', 'status')

    # Check for existing html file
    def change_view(self, request, object_id, form_url='', extra_context=None):
        article = Article.objects.filter(id=object_id)[0]
        article_file_path = f'{get_article_dir_path()}' \
                            f'/{article.page_name}.html'
        article_html = read_article_html_text(article_file_path)
        print(article_html)
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    # Save new or update existing model
    def save_model(self, request, obj, form, change):
        # Article Page Content
        html_content = '{% extends "../article_base.html" %}' \
                       '{% block article_content %}' + \
                        str(form["content"].value()) + \
                       '{% endblock %}'

        # Get article file name and dir to save html file
        article_dir_path = get_article_dir_path()
        article_file_name = get_article_file_name(str(form['title'].value()))

        # Delete an existing file
        remove_file(f'{article_dir_path}/{obj.page_name}.html')

        # Create a new article file
        article_file = open(f'{article_dir_path}'
                            f'/{article_file_name}.html', 'w')
        article_file.write(html_content)
        article_file.close()

        # Map newly created article file name in the database
        obj.page_name = article_file_name

        # Update read time for the article
        obj.read_time = get_article_read_time_from_html(html_content)

        super().save_model(request, obj, form, change)

    # Soft delete model
    def delete_model(self, request, obj):
        obj.status = 'w'
        obj.last_updated = timezone.now()
        obj.save()

    # Soft delete model
    def delete_queryset(self, request, queryset):
        queryset.update(status='w', last_updated=timezone.now())

    # Update article status to Draft
    def make_draft(modeladmin, request, queryset):
        queryset.update(status='d', last_updated=timezone.now())
    make_draft.short_description = "Draft selected articles"

    # Update article status to Published
    def make_published(modeladmin, request, queryset):
        queryset.update(status='p', last_updated=timezone.now())
    make_published.short_description = "Publish selected articles"

    # Update article status to Withdrawn
    def make_withdrawn(modeladmin, request, queryset):
        queryset.update(status='w', last_updated=timezone.now())
    make_withdrawn.short_description = "Withdraw selected articles"

    # Update article read time
    def update_readtime(modeladmin, request, queryset):
        for article in queryset:
            Article.objects.filter(id=article.id). \
                update(
                    read_time=get_article_read_time_from_file(
                        request,
                        article.page_name
                    ),
                    last_updated=timezone.now()
                )
    update_readtime.short_description = "Update the read time"

    actions = [make_draft, make_published, make_withdrawn, update_readtime]


# Register custom model with AdminModel
admin.site.register(Article, ArticleAdmin)
admin.site.index_title = 'Setup.com administration'
