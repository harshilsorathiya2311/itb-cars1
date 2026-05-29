"""
ASGI config for Yourcars project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yourcars.settings')

application = get_asgi_application()
