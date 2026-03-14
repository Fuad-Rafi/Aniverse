import os
import sys

# Add the project root to sys.path so Django can find its packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aniverse.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
