import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, Room  # Import your models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, message):
        user = self.scope["user"]
        room = Room.objects.get(id=self.room_id)
        message = Message.objects.create(
            user=user,
            room=room,
            body=message
        )
        # Add user to participants
        room.participants.add(user)
        return message

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Save message to database
            saved_message = await self.save_message(message)
            
            # Get user info
            user = self.scope["user"]
            time_difference = timezone.now() - saved_message.created
            minutes_ago = int(time_difference.total_seconds() // 60)
            if minutes_ago == 0:
                time_display = "Just now"
            else:
                time_display = f"{minutes_ago} min ago" if minutes_ago < 60 else f"{minutes_ago // 60} hr ago"
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'user_avatar': user.avatar.url if user.avatar else None,
                    'timestamp': time_display,
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'username': event['username'],
                'user_avatar': event['user_avatar'],
                'timestamp': event['timestamp'],
            }))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")