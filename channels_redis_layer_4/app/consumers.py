from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync
from . models import Chat, Group
from channels.db import database_sync_to_async



# all method are called automatically
# all method are called automatically
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Async web socket connected...',  event)
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        print("group name...", self.scope['url_route']['kwargs']['groupname'])
        
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        
        print('self.group_name============', self.group_name)
        
        # self.channels_layer.group_add()   it deafult async ..
        # async_to_sync use convert 
        
        async_to_sync(self.channel_layer.group_add)(
             self.group_name,    #group name
             self.channel_name  #channels name
            )
        self.send({
            'type': 'websocket.accept'
    })

    
    def websocket_receive(self, event):
        print('Massaged Received...',  event['text'])
        
        data = json.loads(event['text'])
        print('python dict... = ', data)
        print('type.... ', type(data))
        print('actual message...', data['msg'])
        group = Group.objects.get(name = self.group_name)
        print('user...', self.scope['user'])
        
        
        if self.scope['user'].is_authenticated:
        
        
            chat=Chat(
                content = data['msg'],
                group = group
            )
            
            chat.save()
            data['user'] = self.scope['user'].username
            print("Complete Data...",data)
            print("Type of Complete Data .. . ", type(data))
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Logger required", "user": "Unknown"})
            })    
    
    
    def chat_message(self, event):
        print('Event...---===', event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
       
            
    
    def websocket_disconnect(self, event):
        # it occur when closing connect or lost connect from client side or server side
        print('Async disconnected...', event)
        
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, 
             self.channel_name
            )
        
        raise StopConsumer()
        


# all method are called automatically
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Async web socket connected...',  event)
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        # self.channels_layer.group_add()   it deafult async ..
        # async_to_sync use convert 
        
        await self.channel_layer.group_add(
            self.group_name,    #group name
             self.channel_name  #channels name
            )
        await self.send({
            'type': 'websocket.accept'
    })

    
    async def websocket_receive(self, event):
        print('Massaged Received...',  event['text'])
        
        data = json.loads(event['text'])
        print('python dict... = ', data)
        print('type.... ', type(data))
        print('actual message...', data['msg'])
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        print('user...', self.scope['user'])
        
        
        if self.scope['user'].is_authenticated:
            chat=Chat(
                content = data['msg'],
                group = group
            )
            
            await database_sync_to_async(chat.save)()
            data['user'] = self.scope['user'].username
            print("Complete Data...",data)
            print("Type of Complete Data .. . ", type(data))
            self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Logger required", "user": "Unknown"})
            })  
            
            
    async def chat_message(self, event):
        print('Event...---===', event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
       
            
    
    async def websocket_disconnect(self, event):
        # it occur when closing connect or lost connect from client side or server side
        print('Async disconnected...', event)
        
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        await self.channel_layer.group_discard(
            self.group_name, 
             self.channel_name
            )
        
        raise StopConsumer()
    