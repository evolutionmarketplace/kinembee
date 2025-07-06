"""
Views for chat.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Prefetch
from django.utils import timezone
from .models import Conversation, Message, PriceOffer, ChatBlock, ChatReport
from .serializers import (
    ConversationSerializer, MessageSerializer, MessageCreateSerializer,
    PriceOfferSerializer, PriceOfferCreateSerializer, ChatReportSerializer,
    ConversationCreateSerializer
)
from apps.core.pagination import CustomPageNumberPagination


class ConversationListView(generics.ListCreateAPIView):
    """
    List user's conversations and create new ones.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            participants=user,
            is_active=True
        ).prefetch_related(
            'participants',
            'product',
            Prefetch('messages', queryset=Message.objects.order_by('-created_at')[:1])
        ).distinct().order_by('-last_message_at', '-created_at')


class ConversationDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageListView(generics.ListCreateAPIView):
    """
    List messages in a conversation and create new ones.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        
        # Verify user is participant
        conversation = Conversation.objects.filter(
            id=conversation_id,
            participants=self.request.user
        ).first()
        
        if not conversation:
            return Message.objects.none()
        
        # Mark messages as read
        Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=self.request.user).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Message.objects.filter(conversation=conversation).order_by('created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        conversation_id = self.kwargs['conversation_id']
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=self.request.user
            )
            context['conversation'] = conversation
        except Conversation.DoesNotExist:
            pass
        return context


class PriceOfferListView(generics.ListCreateAPIView):
    """
    List price offers in a conversation and create new ones.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PriceOfferCreateSerializer
        return PriceOfferSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return PriceOffer.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        conversation_id = self.kwargs['conversation_id']
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=self.request.user
            )
            context['conversation'] = conversation
            context['product'] = conversation.product
        except Conversation.DoesNotExist:
            pass
        return context


class PriceOfferDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and respond to price offers.
    """
    serializer_class = PriceOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PriceOffer.objects.filter(
            Q(offerer=self.request.user) | Q(recipient=self.request.user)
        )

    def update(self, request, *args, **kwargs):
        offer = self.get_object()
        action = request.data.get('action')
        response_message = request.data.get('response_message', '')
        
        if offer.recipient != request.user:
            return Response(
                {'error': 'You can only respond to offers made to you'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if offer.status != 'pending':
            return Response(
                {'error': 'This offer has already been responded to'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if offer.is_expired:
            return Response(
                {'error': 'This offer has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if action == 'accept':
            offer.accept(response_message)
        elif action == 'decline':
            offer.decline(response_message)
        elif action == 'counter':
            counter_price = request.data.get('counter_price')
            if not counter_price:
                return Response(
                    {'error': 'Counter price is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            offer.counter(counter_price, response_message)
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(PriceOfferSerializer(offer).data)


class ChatBlockView(APIView):
    """
    Block/unblock users from messaging.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Block a user."""
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            blocked_user = User.objects.get(id=user_id)
            
            if blocked_user == request.user:
                return Response(
                    {'error': 'You cannot block yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            block, created = ChatBlock.objects.get_or_create(
                blocker=request.user,
                blocked=blocked_user,
                defaults={'reason': request.data.get('reason', '')}
            )
            
            if created:
                return Response({'message': 'User blocked successfully'})
            else:
                return Response({'message': 'User is already blocked'})
                
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        """Unblock a user."""
        try:
            block = ChatBlock.objects.get(
                blocker=request.user,
                blocked_id=user_id
            )
            block.delete()
            return Response({'message': 'User unblocked successfully'})
        except ChatBlock.DoesNotExist:
            return Response({'error': 'User is not blocked'}, status=status.HTTP_404_NOT_FOUND)


class ChatReportView(generics.CreateAPIView):
    """
    Report inappropriate chat behavior.
    """
    serializer_class = ChatReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        conversation_id = self.kwargs['conversation_id']
        reported_user_id = self.kwargs['user_id']
        
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=self.request.user
            )
            from django.contrib.auth import get_user_model
            User = get_user_model()
            reported_user = User.objects.get(id=reported_user_id)
            
            context['conversation'] = conversation
            context['reported_user'] = reported_user
        except (Conversation.DoesNotExist, User.DoesNotExist):
            pass
        
        return context


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_stats(request):
    """
    Get chat statistics for the user.
    """
    user = request.user
    
    stats = {
        'total_conversations': Conversation.objects.filter(participants=user).count(),
        'unread_messages': Message.objects.filter(
            conversation__participants=user,
            is_read=False
        ).exclude(sender=user).count(),
        'active_offers': PriceOffer.objects.filter(
            Q(offerer=user) | Q(recipient=user),
            status='pending'
        ).count(),
        'blocked_users': ChatBlock.objects.filter(blocker=user).count(),
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_conversation_read(request, conversation_id):
    """
    Mark all messages in a conversation as read.
    """
    try:
        conversation = Conversation.objects.get(
            id=conversation_id,
            participants=request.user
        )
        
        count = Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=request.user).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({'message': f'{count} messages marked as read'})
        
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_conversation(request, conversation_id):
    """
    Archive a conversation.
    """
    try:
        conversation = Conversation.objects.get(
            id=conversation_id,
            participants=request.user
        )
        
        conversation.is_archived = True
        conversation.save()
        
        return Response({'message': 'Conversation archived'})
        
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)