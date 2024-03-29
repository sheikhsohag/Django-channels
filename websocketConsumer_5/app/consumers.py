from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . models import Chat, Group
from channels.db import database_sync_to_async

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
        group = Group.objects.get(name = self.group_name)
        print("ok=====================")
        
        print(self.scope['user'],'================')
        
        if self.scope['user'].is_authenticated:
            content = Chat(
                content = data["msg"],
                group = group,
                user = self.scope['user']
            )
            
            content.save()
            data['user'] = self.scope['user'].username
            
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
            
        else:
            self.send(text_data=json.dumps({
                'msg': "LongIn Required"
            }))
            
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
        
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        
        
        if self.scope['user'].is_authenticated:
            contents = Chat(
                content = data["msg"],
                group = group,
                user = self.scope['user']
            )
            
            await database_sync_to_async(contents.save)()
            data['user'] = self.scope['user'].username
            
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                "msg": "Login Required"
            }))
        
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