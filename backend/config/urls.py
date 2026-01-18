
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Import viewsets
from apps.documents.views import DocumentCollectionViewSet, DocumentViewSet
from apps.chat.views import ConversationViewSet, MessageViewSet
from apps.users.views import UserViewSet

# Create router
router = DefaultRouter()
router.register(r'collections', DocumentCollectionViewSet, basename='collection')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/login/', obtain_auth_token, name='api_login'),
    
    # Authentication
    path('api/v1/auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)