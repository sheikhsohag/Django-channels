from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from time import sleep
import asyncio
# from asgiref.sync import async_to_sync
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from . models import Chat,Group
from channels.db import database_sync_to_async

class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        print('websocket Connetcted...')
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(self.group_name,
             self.channel_name 
            )
        self.accept()
        # self.close()   #to reject the connections
        
        
        
    def receive_json(self, content, **kwargs):
        print('Message received from client....', content)
        # this content is dict formmat because of used jsonWebsocketconsumer..
        # otherwise we get string type 
        print('Type of Content...', type(content))
        print('Actual message...', content['msg'])
        
        group = Group.objects.get(name=self.group_name)
        # user = self.scope['user']
        # user = User.objects.get(username=user)
        
        chat = Chat(
            content = content['msg'],
            # user = user,
            group = group
        )
        
        chat.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',
                'message': content['msg']
            }
        )
        
    def chat_message(self, event):
        print('Event ...', event)
        self.send_json({
            'msg': event['message']
        })

        
    def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        print('websocket Connetcted...')
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        # self.close()   #to reject the connections
        
        
    async def receive_json(self, content, **kwargs):
        print('Message received from client...a.', content)
        # this content is dict formmat because of used jsonWebsocketconsumer..
        # otherwise we get string type
        
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        # user = self.scope['user']
        # user = User.objects.get(username=user)
        
        chat = Chat(
            content = content['msg'],
            # user = user,
            group = group
        )
        
        database_sync_to_async(chat.save)()
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': content['msg']
            }
        ) 
    async def chat_message(self, event):
        await self.send_json({
            'msg':event['message']
        })

        
    async def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)
        
    