from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Room, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        username = text_data_json['username']
        user_avatar = text_data_json['user_avatar']

        # Save the message in the database
        room = Room.objects.get(id=self.room_id)
        user = User.objects.get(id=user_id)
        Message.objects.create(user=user, room=room, body=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user.id,
                'username': username,
                'user_avatar': user.avatar.url,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        username = event['username']
        user_avatar = event['user_avatar']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user_id': user_id,
            'username': username,
            'user_avatar': user_avatar
        }))
