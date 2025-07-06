"""
WebSocket consumers for real-time chat.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time chat.
    """
    
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        # Check if user is participant in conversation
        if await self.is_participant():
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            content = data['content']
            
            # Save message to database
            message = await self.save_message(content)
            
            if message:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': {
                            'id': str(message.id),
                            'content': message.content,
                            'sender': {
                                'id': str(message.sender.id),
                                'name': message.sender.full_name
                            },
                            'created_at': message.created_at.isoformat(),
                            'message_type': message.message_type
                        }
                    }
                )
        
        elif message_type == 'typing':
            # Broadcast typing indicator
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': str(self.scope['user'].id),
                    'is_typing': data.get('is_typing', False)
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))

    async def typing_indicator(self, event):
        # Don't send typing indicator to the sender
        if str(self.scope['user'].id) != event['user_id']:
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator',
                'user_id': event['user_id'],
                'is_typing': event['is_typing']
            }))

    @database_sync_to_async
    def is_participant(self):
        """Check if user is a participant in the conversation."""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return conversation.participants.filter(id=self.scope['user'].id).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        """Save message to database."""
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=self.scope['user'],
                content=content,
                message_type='text'
            )
            
            # Update conversation last message
            conversation.last_message = content
            conversation.last_message_at = message.created_at
            conversation.save()
            
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            return None