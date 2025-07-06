"""
Custom middleware for Evolution Digital Market.
"""
import logging
import time
import uuid
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all requests and responses.
    """
    
    def process_request(self, request):
        """
        Log incoming requests.
        """
        request.start_time = time.time()
        request.request_id = str(uuid.uuid4())
        
        logger.info(
            f"Request {request.request_id}: {request.method} {request.get_full_path()} "
            f"from {self.get_client_ip(request)}"
        )
        
    def process_response(self, request, response):
        """
        Log outgoing responses.
        """
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Response {getattr(request, 'request_id', 'unknown')}: "
                f"{response.status_code} in {duration:.3f}s"
            )
        
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CORSMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware for additional control.
    """
    
    def process_response(self, request, response):
        """
        Add CORS headers to response.
        """
        if settings.DEBUG:
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response['Access-Control-Allow-Credentials'] = 'true'
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to responses.
    """
    
    def process_response(self, request, response):
        """
        Add security headers.
        """
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response