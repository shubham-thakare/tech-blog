from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from apps.website.models.article import Article
from apps.website.models.inbox import Inbox
from apps.website.models.comments import Comments
from apps.website.helpers.utils import get_host_uri_with_http, \
    time_ago, notify_on_email
from django.contrib.postgres.search import SearchRank, \
    SearchVector, SearchQuery
import re


def search_articles(query):
    processed_query = re.sub(r'[^\w.\-:;,]', ' ', query)

    if processed_query:
        search_vector = SearchVector('title', 'keywords')

        search_query = SearchQuery(processed_query)
        processed_query = processed_query.split(' ')

        if len(processed_query) > 1:
            for keyword in processed_query:
                search_query |= SearchQuery(keyword)

        search_rank = SearchRank(search_vector, search_query)

        articles = Article.objects \
            .annotate(search=search_vector, rank=search_rank) \
            .filter(status='p', search=search_query) \
            .order_by('-rank')

        for article in articles:
            article.time_ago = article.created_at.date()

        return articles
    else:
        return {}


def index(request):
    articles = Article.objects.filter(status='p').order_by('-created_at')

    for article in articles:
        article.time_ago = article.created_at.date()

    context = {
        'articles': articles,
        'articles_length': len(articles)
    }

    return render(request, 'website/index.html', context)


def search(request):
    query = request.GET['query']
    articles = search_articles(query)

    context = {
        'query': query,
        'articles': articles,
        'articles_length': len(articles)
    }
    return render(request, 'website/search.html', context)


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
                name=str(name["value"]).title(),
                email=email['value'],
                message=message['value']
            )
            contact_details.save()

            # Send notification mail for contact request
            mail_subject = 'SetupFAQ - Someone is trying to contact you'
            mail_body = f'***********************************************\n' \
                        f'Visitor\'s Name: {str(name["value"]).title()}\n' \
                        f'Visitor\'s Email: {email["value"]}\n' \
                        f'Message:\n' \
                        f'{message["value"]}\n' \
                        f'***********************************************'
            notify_on_email(mail_subject, mail_body)

            return render(request, 'website/contact_us.html', {'sent': True})

    return render(request, 'website/contact_us.html', {
        'name': name,
        'email': email,
        'message': message,
    })


def article_base(request, article_id, page_name):
    try:
        name = {'invalid': '', 'value': ''}
        email = {'invalid': '', 'value': ''}
        comments = {'invalid': '', 'value': ''}

        article_data = get_object_or_404(Article, id=article_id,
                                         status='p', page_name=page_name)

        related_articles = search_articles(article_data.title)
        related_articles = related_articles.exclude(id=article_id)[:3]

        for article in related_articles:
            article.time_ago = article.created_at.date()

        if request.method == 'POST':
            if not request.POST.get('name', ''):
                name['invalid'] = 'is-invalid'

            if request.POST.get('email') \
                    and '@' not in request.POST['email'] \
                    or '.' not in request.POST['email']:
                email['invalid'] = 'is-invalid'

            if not request.POST.get('comments', '') or \
                    not len(request.POST['comments']) >= 0:
                comments['invalid'] = 'is-invalid'

            name['value'] = request.POST['name']
            email['value'] = request.POST['email']
            comments['value'] = request.POST['comments']

            if not name['invalid'] and not email['invalid'] and \
                    not comments['invalid']:
                comment_details = Comments(
                    article=article_data,
                    name=str(name['value']).title().strip(),
                    email=email['value'],
                    comments=comments['value']
                )
                comment_details.save()

                # Send notification mail for comments
                mail_subject = 'SetupFAQ - Someone has commented on article'
                mail_body = f'*******************************************\n' \
                            f'Article ID: {article_id}\n' \
                            f'Article Title: {article_data.title}\n' \
                            f'*******************************************\n' \
                            f'Reader\'s Name: {str(name["value"]).title()}\n'\
                            f'Reader\'s Email: {email["value"]}\n' \
                            f'Comments:\n' \
                            f'{comments["value"]}\n' \
                            f'*******************************************'
                notify_on_email(mail_subject, mail_body)

                return HttpResponseRedirect(f'{request.get_full_path()}'
                                            f'#comments_start')

        article_comments = Comments.objects \
            .filter(article=article_id, status='SH') \
            .order_by('-submitted_on')

        for comment in article_comments:
            comment.submitted_on = time_ago(comment.submitted_on.timestamp())

        context = {
            'md_file': page_name,
            'public_keywords': article_data.keywords,
            'tags': str(article_data.keywords).split(','),
            'public_title': article_data.title,
            'public_description': article_data.description,
            'public_image': f'{get_host_uri_with_http(request)}'
                            f'{article_data.public_image}',
            'created_at': article_data.created_at.date(),
            'read_time': article_data.read_time,
            'share_url': request.build_absolute_uri(),
            'related_articles': related_articles,
            'related_articles_length': len(related_articles),
            'page_type': 'article',
            'is_article': True,
            'published_time': article_data.created_at,
            'modified_time': article_data.last_updated,
            'name': name,
            'email': email,
            'comments': comments,
            'article_comments': article_comments,
            'article_comments_length': len(article_comments),
        }

        article_data.views += 1
        article_data.save()
        return render(request, f'website/articles/{page_name}.html', context)
    except Exception:
        raise Http404()
