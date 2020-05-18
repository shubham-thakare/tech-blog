from django.shortcuts import render


def index(request):
    context = {
        'message': 'Hello, this is a demo page.',
    }
    return render(request, 'website/index.html', context)
