"""
URL configuration for Evolution Digital Market project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.core.views import HealthCheckView

# API Router
router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # API endpoints
    path('api/v1/', include([
        path('auth/', include('apps.accounts.urls')),
        path('products/', include('apps.products.urls')),
        path('categories/', include('apps.categories.urls')),
        path('reviews/', include('apps.reviews.urls')),
        path('notifications/', include('apps.notifications.urls')),
        path('payments/', include('apps.payments.urls')),
        path('chat/', include('apps.chat.urls')),
        path('analytics/', include('apps.analytics.urls')),
        path('support/', include('apps.support.urls')),
    ])),
    
    # Django allauth
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Custom admin configuration
admin.site.site_header = 'Evolution Digital Market Admin'
admin.site.site_title = 'Evolution Market'
admin.site.index_title = 'Administration'