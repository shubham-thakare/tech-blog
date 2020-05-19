from django.shortcuts import render


def index(request):
    context = {
        'message': 'Hello, this is a demo page.',
    }
    return render(request, 'website/index.html', context)


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html', None)


def terms_and_conditions(request):
    return render(request, 'website/terms_and_conditions.html', None)


def sitemap(request):
    return render(request, 'website/sitemap.html', None)
