from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blake.settings')

app = Celery('blake')

# Read Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in apps
app.autodiscover_tasks()
