from django.contrib import admin
from apps.website.models.article import Article
from apps.website.models.inbox import Inbox
from django.utils import timezone
from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from apps.website.helpers.utils import get_article_read_time_from_file, \
    get_article_read_time_from_html, \
    get_article_dir_path, get_article_file_name, \
    remove_file, read_article_html_text


admin.site.index_title = 'SetupFAQ administration'


class ArticleAdminForm(forms.ModelForm):
    content = RichTextUploadingFormField(required=False)

    class Meta:
        model = Article
        fields = [
            'page_name',
            'title',
            'keywords',
            'description',
            'public_image',
            'status'
        ]

    def get_initial_for_field(self, field, field_name):
        try:
            # Adding existing html into the CKEditor
            page_name = self.initial['page_name']
            if page_name:
                article_file_path = f'{get_article_dir_path()}' \
                                    f'/{page_name}.html'
                raw_html = read_article_html_text(article_file_path)
                self.initial['content'] = raw_html
        except Exception:
            pass

        return super(ArticleAdminForm, self) \
            .get_initial_for_field(field, field_name)


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ['title', 'status', 'last_updated']
    search_fields = ('id', 'title', 'status')
    list_filter = ('status', 'created_at', 'last_updated',)
    date_hierarchy = 'last_updated'
    ordering = ('-last_updated',)

    fieldsets = [
        ['General Information', {
            'fields': [
                'title',
                'keywords',
                'description',
                'public_image',
                'status',
                'content'
            ]
        }],
        ['Template Page Information (Optional)', {
            'classes': ['collapse'],
            'fields': ['page_name'],
        }],
    ]

    # Save new or update existing model
    def save_model(self, request, obj, form, change):
        # Article Page Content
        html_content = '{% extends "../article_base.html" %}\n' \
                       '{% block article_content %}\n' + \
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

    # Don't delete articles
    def has_delete_permission(self, request, obj=None):
        return False

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


class InboxAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'submitted_on', 'status']
    ordering = ('-status',)
    search_fields = ('name', 'email')
    list_filter = ('submitted_on',)
    date_hierarchy = 'submitted_on'

    # Update message status to seen
    def mark_as_seen(modeladmin, request, queryset):
        queryset.update(status='SN')
    mark_as_seen.short_description = "Mark selected messages as seen"

    # Update message status to seen
    def mark_as_unseen(modeladmin, request, queryset):
        queryset.update(status='UN')
    mark_as_unseen.short_description = "Mark selected messages as unseen"

    # Deon't delete messages
    def has_delete_permission(self, request, obj=None):
        return False

    actions = [mark_as_seen, mark_as_unseen]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Inbox, InboxAdmin)

# Globally disable delete selected
admin.site.disable_action('delete_selected')
