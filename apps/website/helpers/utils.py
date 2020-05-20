from django.utils import timezone
from django.templatetags.tz import register
import math


@register.simple_tag
def time_ago(time):
    time_formats = [
        [60, 'seconds', 1],  # 60
        [120, '1 minute ago', '1 minute from now'],  # 60*2
        [3600, 'minutes', 60],  # 60*60, 60
        [7200, '1 hour ago', '1 hour from now'],  # 60*60*2
        [86400, 'hours', 3600],  # 60*60*24, 60*60
        [172800, 'yesterday', 'tomorrow'],  # 60*60*24*2
        [604800, 'days', 86400],  # 60*60*24*7, 60*60*24
        [1209600, 'last week', 'next week'],  # 60*60*24*7*4*2
        [2419200, 'weeks', 604800],  # 60*60*24*7*4, 60*60*24*7
        [4838400, 'last month', 'next month'],  # 60*60*24*7*4*2
        [29030400, 'months', 2419200],  # 60*60*24*7*4*12, 60*60*24*7*4
        [58060800, 'last year', 'next year'],  # 60*60*24*7*4*12*2
        [2903040000, 'years', 29030400],  # 60*60*24*7*4*12*100, 60*60*24*7*4*12
        [5806080000, 'last century', 'next century'],  # 60*60*24*7*4*12*100*2
        [58060800000, 'centuries', 2903040000]  # 60*60*24*7*4*12*100*20, 60*60*24*7*4*12*100
    ]

    current_time = timezone.now().timestamp()
    seconds = (current_time - time)
    token = 'ago'
    list_choice = 1

    if seconds == 0:
        return 'just now'

    if seconds < 0:
        seconds = math.fabs(seconds)
        token = 'from now'
        list_choice = 2

    for time_format in time_formats:
        if seconds < time_format[0]:
            if type(time_format[2]) is str:
                return time_format[list_choice]
            else:
                return f"{math.floor(seconds / time_format[2])} {time_format[1]} {token}"

    return None
