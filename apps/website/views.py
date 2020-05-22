from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from apps.website.models.article import Article
from apps.website.models.inbox import Inbox
from apps.website.helpers.utils import get_host_uri_with_http


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
    name = {'invalid': '', 'value': ''}
    email = {'invalid': '', 'value': ''}
    message = {'invalid': '', 'value': ''}

    if request.method == 'POST':
        if not request.POST.get('name', ''):
            name['invalid'] = 'is-invalid'

        if request.POST.get('email') \
                and '@' not in request.POST['email'] \
                or '.' not in request.POST['email']:
            email['invalid'] = 'is-invalid'

        if not request.POST.get('message', '') or \
                not len(request.POST['message']) >= 20:
            message['invalid'] = 'is-invalid'

        name['value'] = request.POST['name']
        email['value'] = request.POST['email']
        message['value'] = request.POST['message']

        if not name['invalid'] and not email['invalid'] and \
                not message['invalid']:
            contact_details = Inbox(
                name=name['value'],
                email=email['value'],
                message=message['value']
            )
            contact_details.save()

            return HttpResponseRedirect('/view/contact-us')

    return render(request, 'website/contact_us.html', {
        'name': name,
        'email': email,
        'message': message,
    })


def article_base(request, article_id, page_name):
    try:
        article_data = get_object_or_404(Article, id=article_id,
                                         status='p', page_name=page_name)

        related_articles = Article.objects.all()[:3]
        for article in related_articles:
            article.time_ago = article.created_at.date()

        context = {
            'md_file': page_name,
            'public_keywords': article_data.keywords,
            'public_title': article_data.title,
            'public_description': article_data.description,
            'public_image': f'{get_host_uri_with_http(request)}'
                            f'{article_data.public_image}',
            'created_at': article_data.created_at.date(),
            'read_time': article_data.read_time,
            'share_url': request.build_absolute_uri(),
            'related_articles': related_articles,
            'related_articles_length': len(related_articles)
        }

        article_data.views += 1
        article_data.save()
        return render(request, f'website/articles/{page_name}.html', context)
    except Exception as ex:
        print(ex)
        raise Http404()
