import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


from chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def get_room_messages(self,data):
        messages = [model_to_dict(message,) for message in Message.getByRoom(self.room_name)]
        content = {
            'messages' : messages
        }
        self.send_message(content)


    def new_message(self,data):
        username = data['username']
        room = self.scope['url_route']['kwargs']['room_name']
        body = data['message']
        message = Message.createOne(username,room,body)
        content = {
            'command' : 'new_message',
            'message' : model_to_dict(message)
        }
        return self.send_chat_message(content)


    commands = {
        'get_room_messages' : get_room_messages,
        'new_message' : new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data) 

    def send_chat_message(self,message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self,message):
        self.send(text_data=json.dumps(message,cls=DjangoJSONEncoder))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message,cls=DjangoJSONEncoder))