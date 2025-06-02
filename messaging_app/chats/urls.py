from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin

# Initialize the DefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Define URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Maps /api/conversations/ and /api/messages/
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.urls')),  # Updated to reference messaging_app
]