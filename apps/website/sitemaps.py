from django.contrib import sitemaps
from django.urls import reverse
from apps.website.models.article import Article
from apps.website.models.authors import Authors


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'contact_us',
            'privacy_policy',
            'terms_of_service',
            'articles_rss_feed',
        ]

    def location(self, item):
        return reverse(item)


class ArticlesSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Article.objects.filter(status='p').order_by('-last_updated')

    def lastmod(self, item):
        return item.last_updated


class AuthorProfilesSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'yearly'

    def items(self):
        return Authors.objects.filter(status='AC').order_by('-name')
