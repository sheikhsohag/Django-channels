from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync



# all method are called automatically
# all method are called automatically
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Async web socket connected...',  event)
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        # self.channels_layer.group_add()   it deafult async ..
        # async_to_sync use convert 
        
        async_to_sync(self.channel_layer.group_add)(
            'programmers',    #group name
             self.channel_name  #channels name
            )
        self.send({
            'type': 'websocket.accept'
    })

    
    def websocket_receive(self, event):
        print('Massaged Received...',  event['text'])
        async_to_sync(self.channel_layer.group_send)('programmers', {
            'type': 'chat.message',
            'message': event['text']
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
            'programmers', 
             self.channel_name
            )
        
        raise StopConsumer()
        


# all method are called automatically
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Async web socket connected...',  event)
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        # self.channels_layer.group_add()   it deafult async ..
        # async_to_sync use convert 
        
        await self.channel_layer.group_add(
            'programmers',    #group name
             self.channel_name  #channels name
            )
        await self.send({
            'type': 'websocket.accept'
    })

    
    async def websocket_receive(self, event):
        print('Massaged Received...',  event['text'])
        await self.channel_layer.group_send('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })
    
    
    async def chat_message(self, event):
        print('Event...---===', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
       
            
    
    async def websocket_disconnect(self, event):
        # it occur when closing connect or lost connect from client side or server side
        print('Async disconnected...', event)
        
        print("channels Layer...", self.channel_layer)
        
        print("channels name...", self.channel_name)
        
        await self.channel_layer.group_discard(
            'programmers', 
             self.channel_name
            )
        
        raise StopConsumer()