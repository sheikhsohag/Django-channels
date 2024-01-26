from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class MyWebsocketConsumer(WebsocketConsumer):
    
    def connect(self):
        print("Websocket Connected...")
        print("Channels Layer...",self.channel_layer)
        # print("Channels Name...",self.channel_name)
        print("Channels Name...", self.channel_name)
        
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('Group Name...', self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        # self.close() #To reject the connection
        
    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client...', text_data)
        print('===================================')
        data = json.loads(text_data)
        print('======================')
        message = data['msg']
        print('Actual message...', message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )
        
    def chat_message(self,event):
        self.send(text_data = json.dumps({
            'msg': event['message']
        }))
    
    def disconnect(self, close_code):
        print('Disconnected...', close_code)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        
        
class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("AsyncWebsocketConsumer Connected...")
        
        print("Channels Layer...", self.channel_layer)
        print("Channels Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # self.close() #To reject the connection
        
    async def receive(self, text_data=None, bytes_data=None):
        print('AsyncWebsocketConsumer Message Received from Client...', text_data)
        print('Text_data===', text_data)
        print("Type==", type(text_data))
        data = json.loads(text_data)
        print("data....", type(data))
        print('Actual Data...', data["msg"])
        message = data["msg"]
          
        await self.channel_layer.group_send(
            self.group_name,
            
            {
                'type': 'chat.message',
                'message': message
            }
        )
        
    async def chat_message(self, event):
        await self.send( text_data = json.dumps({
            'msg': event['message']
        }))
    
    async def disconnect(self, close_code):
        print('AsyncWebsocketConsumer Disconnected...', close_code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )