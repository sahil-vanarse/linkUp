# base/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Accept the WebSocket connection

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected',
        }))
