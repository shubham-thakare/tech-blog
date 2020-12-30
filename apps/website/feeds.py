from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from apps.website.models.article import Article


class RSSFeed(Feed):
    link = ""
    title = "TechBlog.com articles RSS feed"
    description = "We are here to help you to get " \
                  "everything configured seamlessly."

    def items(self):
        return Article.objects.filter(status='p').order_by('-created_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.description, 30)
