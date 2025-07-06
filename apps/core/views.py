"""
Core views for Evolution Digital Market.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import connection
from django.core.cache import cache
import redis
from django.conf import settings


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Check the health of various services.
        """
        health_status = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'services': {}
        }

        # Check database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status['services']['database'] = 'healthy'
        except Exception as e:
            health_status['services']['database'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # Check Redis
        try:
            cache.set('health_check', 'ok', 30)
            cache.get('health_check')
            health_status['services']['redis'] = 'healthy'
        except Exception as e:
            health_status['services']['redis'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # Check Celery (if configured)
        try:
            from evolution_market.celery import app
            inspect = app.control.inspect()
            stats = inspect.stats()
            if stats:
                health_status['services']['celery'] = 'healthy'
            else:
                health_status['services']['celery'] = 'no workers available'
        except Exception as e:
            health_status['services']['celery'] = f'unhealthy: {str(e)}'

        response_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(health_status, status=response_status)