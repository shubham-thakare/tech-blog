from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from apps.website.feeds import RSSFeed
from apps.website.sitemaps import StaticViewSitemap, ArticlesSitemap, \
    AuthorProfilesSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticlesSitemap,
    'profiles': AuthorProfilesSitemap
}

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('view/contact-us',
         views.contact_us,
         name='contact_us'),
    path('view/privacy-policy',
         views.privacy_policy,
         name='privacy_policy'),
    path('view/terms-of-service',
         views.terms_of_service,
         name='terms_of_service'),
    path('article/<int:article_id>/<str:page_name>',
         views.article_base,
         name='article_base'),
    path('author/<int:author_id>/<str:author_name>',
         views.author,
         name='author_profile'),
    path('article/search',
         views.search,
         name='article_search'),
    path('view/sitemap.xml',
         sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('feeds/rss.xml',
         RSSFeed(),
         name='articles_rss_feed'),
]
