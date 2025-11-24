from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet,MessageViewSet


router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversations')

convo_router = routers.NestedDefaultRouter(router, 'conversations', lookup='conversation')
convo_router.register('messages', MessageViewSet, basename='conversation-messages')
router.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls))
]
