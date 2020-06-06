from django import template
import markdown as md
import os


TEMPLATE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + \
               '/templates/website/articles'


register = template.Library()


@register.simple_tag
def markdown(md_file):
    md_text = open(f'{TEMPLATE_DIR}/{md_file}.md').read()
    return md.markdown(md_text, extensions=['markdown.extensions.fenced_code'])
