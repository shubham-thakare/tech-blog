from django.utils import timezone
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import math
import readtime
import os


def time_ago(time):
    time_formats = [
        [60, 'seconds', 1],
        [120, '1 minute ago', '1 minute from now'],
        [3600, 'minutes', 60],
        [7200, '1 hour ago', '1 hour from now'],
        [86400, 'hours', 3600],
        [172800, 'yesterday', 'tomorrow'],
        [604800, 'days', 86400],
        [1209600, 'last week', 'next week'],
        [2419200, 'weeks', 604800],
        [4838400, 'last month', 'next month'],
        [29030400, 'months', 2419200],
        [58060800, 'last year', 'next year'],
        [2903040000, 'years', 29030400],
        [5806080000, 'last century', 'next century'],
        [58060800000, 'centuries', 2903040000]
    ]

    time = int(str(time).split('.')[0])
    current_time = int(str(timezone.now().timestamp()).split('.')[0])
    seconds = (current_time - time)
    token = 'ago'
    list_choice = 1

    if seconds == 0:
        return 'Just now'

    if seconds < 0:
        seconds = math.fabs(seconds)
        token = 'from now'
        list_choice = 2

    for time_format in time_formats:
        if seconds < time_format[0]:
            if type(time_format[2]) is str:
                return time_format[list_choice]
            else:
                return f"{math.floor(seconds / time_format[2])} " \
                       f"{time_format[1]} {token}"

    return None


def read_article_text(request, file_name: str):
    try:
        html_text = render(request,
                           f'website/articles/{file_name}.html', None).content
        return html_text
    except Exception:
        return ''


def get_article_read_time_from_file(request, file_name: str):
    try:
        read_time = readtime.of_html(read_article_text(request, file_name))
        return read_time
    except Exception:
        return ''


def get_article_read_time_from_html(html_text: str):
    try:
        read_time = readtime.of_html(html_text)
        return read_time
    except Exception:
        return ''


def get_article_dir_path():
    return f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}' \
           f'/templates/website/articles'


def get_article_file_name(title: str):
    timestamp = str(timezone.now().timestamp()).replace(".", "")
    return title \
        .replace('\'', '') \
        .replace('"', '') \
        .replace('.', '') \
        .replace('!', '') \
        .replace('<', '') \
        .replace('>', '') \
        .replace(':', '') \
        .replace('/', '') \
        .replace('\\', '') \
        .replace('?', '') \
        .replace('*', '') \
        .replace(' ', '-') \
        .lower() + '_' + timestamp


def get_filename(filename: str):
    filename = filename.split('.')
    filename = f'{str(timezone.now().timestamp()).replace(".", "")}' \
               f'.{filename[len(filename)-1]}'
    return filename


def remove_file(file_path: str):
    try:
        os.remove(file_path)
    except Exception:
        pass


def read_article_html_text(file_path: str):
    try:
        html_text = str(open(file_path).read()) \
            .replace('{% extends "../article_base.html" %}', '') \
            .replace('{% block article_content %}', '') \
            .replace('{% endblock %}', '')
        return html_text
    except Exception:
        return ''


def get_host_uri_with_scheme(request):
    absolute_uri = str(request.build_absolute_uri()).split('/')
    return f'{absolute_uri[0]}//{absolute_uri[2]}'


def notify_on_email(subject, message):
    try:
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.WEBSITE_ADMIN_EMAIL]
        send_mail(subject, message, email_from, recipient_list)
    except Exception:
        pass
