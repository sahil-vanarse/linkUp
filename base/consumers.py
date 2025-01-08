# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from aiokafka import AIOKafkaProducer
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        try:
            # Initialize Kafka producer
            self.producer = AIOKafkaProducer(
                bootstrap_servers='localhost:9092',
                enable_idempotence=True
            )
            await self.producer.start()
        except Exception as e:
            print(f"Kafka producer error: {e}")
            # Continue even if Kafka fails - we can still handle WebSocket chat

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Stop Kafka producer if it exists
        if hasattr(self, 'producer'):
            await self.producer.stop()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        try:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            # Try to send to Kafka if producer exists
            if hasattr(self, 'producer'):
                try:
                    await self.producer.send_and_wait(
                        'chat_topic', 
                        message.encode('utf-8')
                    )
                except Exception as e:
                    print(f"Kafka send error: {e}")
                    # Continue even if Kafka fails
        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))