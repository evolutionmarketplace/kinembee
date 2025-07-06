"""
URL configuration for chat app.
"""
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Conversations
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:conversation_id>/archive/', views.archive_conversation, name='archive-conversation'),
    path('conversations/<uuid:conversation_id>/mark-read/', views.mark_conversation_read, name='mark-conversation-read'),
    
    # Messages
    path('conversations/<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    
    # Price offers
    path('conversations/<uuid:conversation_id>/offers/', views.PriceOfferListView.as_view(), name='price-offer-list'),
    path('offers/<uuid:pk>/', views.PriceOfferDetailView.as_view(), name='price-offer-detail'),
    
    # Blocking and reporting
    path('block/<uuid:user_id>/', views.ChatBlockView.as_view(), name='chat-block'),
    path('conversations/<uuid:conversation_id>/report/<uuid:user_id>/', views.ChatReportView.as_view(), name='chat-report'),
    
    # Statistics
    path('stats/', views.chat_stats, name='chat-stats'),
]