"""
WSGI config for Evolution Digital Market project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution_market.settings.production')

application = get_wsgi_application()