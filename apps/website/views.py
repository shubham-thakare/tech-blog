from django.shortcuts import render, get_object_or_404
from django.http import Http404
from apps.website.models.article import Article


def index(request):
    articles = Article.objects.filter(status='p').order_by('-created_at')

    for article in articles:
        article.time_ago = article.created_at.date()

    context = {
        'articles': articles
    }
    return render(request, 'website/index.html', context)


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html', None)


def terms_of_service(request):
    return render(request, 'website/terms_of_service.html', None)


def contact_us(request):
    return render(request, 'website/contact_us.html', None)


def article_base(request, article_id, page_name):
    try:
        article_data = get_object_or_404(Article, id=article_id,
                                         status='p', page_name=page_name)

        context = {
            'md_file': page_name,
            'public_keywords': article_data.keywords,
            'public_title': article_data.title,
            'public_description': article_data.description,
            'public_image': article_data.public_image,
            'created_at': article_data.created_at.date(),
            'read_time': article_data.read_time,
        }

        article_data.views += 1
        article_data.save()
        return render(request, f'website/articles/{page_name}.html', context)
    except Exception as ex:
        print(ex)
        raise Http404()
