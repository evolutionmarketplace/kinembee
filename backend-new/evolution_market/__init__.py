# Evolution Digital Market Backend
from .celery import app as celery_app

__all__ = ('celery_app',)