from django import template
from apps.website.models.article import Article


register = template.Library()


@register.simple_tag
def random_articles():
    articles = Article.objects.filter(status="p").order_by('?')[:3]

    for article in articles:
        article.time_ago = article.created_at.date()

    context = {
        'articles': articles,
        'articles_length': len(articles),
    }

    return context
