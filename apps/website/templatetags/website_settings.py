from django import template
from apps.website.models.settings import WebsiteSettings


register = template.Library()


@register.simple_tag
def is_under_maintenance():
    website_settings = WebsiteSettings.objects.first()

    if website_settings and website_settings.under_maintenance:
        return True

    return False
