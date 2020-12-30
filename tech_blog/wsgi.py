"""
WSGI config for tech_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tech_blog.settings')

logger = logging.getLogger(__name__)
logger.info("Starting wsgi server for the setup.com application.")

application = get_wsgi_application()
