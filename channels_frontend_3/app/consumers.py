from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json



# all method are called automatically
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        # it is first time called when user connected initially
        print('web socket connected...',  event)
        
        self.send({
            'type': 'websocket.accept'
        })
    
    # def websocket_receive(self, event):
    #     # when client sent data
    #     print('Massaged Received...',  event)
    #     print('Massaged is',  event['text'])
    #     for i in range(50):
    #         self.send({
    #         'type': 'websocket.send',
    #         'text': str(i)
    #          })
    #         sleep(1)
    
    def websocket_receive(self, event):
        # when client sent data
        print('Massaged Received...',  event)
        print('Massaged is',  event['text'])
        for i in range(50):
            self.send({
            'type': 'websocket.send',
            'text': json.dumps({"count": i})
             })
            sleep(1)
    
    def websocket_disconnect(self, event):
        # it occur when closing connect or lost connect from client side or server side
        print('disconnected...',  event)
        raise StopConsumer()
        


# all method are called automatically
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        # it is first time called when user connected initially
        print('Async web socket connected...',  event)
        await self.send({
            'type': 'websocket.accept'
        })
    
    # async def websocket_receive(self, event):
    #     # when client sent data
    #     print('Massaged Received...',  event)
    #     print('Async Message is ', event['type'])
    #     for i in range(10):
    #         await self.send({
    #         'type': 'websocket.send',
    #         'text': str(i)
    #          })
    #         await asyncio.sleep(1)
    
    async def websocket_receive(self, event):
        # when client sent data
        print('Massaged Received...',  event)
        print('Async Message is ', event['type'])
        for i in range(10):
            await self.send({
            'type': 'websocket.send',
            'text': json.dumps({"count": i})
             })
            await asyncio.sleep(1)
            
    
    async def websocket_disconnect(self, event):
        # it occur when closing connect or lost connect from client side or server side
        print('Async disconnected...', event)
        raise StopConsumer()