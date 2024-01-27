from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from time import sleep
import asyncio

class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        print('websocket Connetcted...')
        self.accept()
        # self.close()   #to reject the connections
        
        
    def receive_json(self, content, **kwargs):
        print('Message received from client....', content)
        # this content is dict formmat because of used jsonWebsocketconsumer..
        # otherwise we get string type 
        for i in range(20):
            self.send_json({
                'message':str(i)
            })
            sleep(1)
        
    def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        print('websocket Connetcted...')
        await self.accept()
        # self.close()   #to reject the connections
        
        
    async def receive_json(self, content, **kwargs):
        print('Message received from client...a.', content)
        # this content is dict formmat because of used jsonWebsocketconsumer..
        # otherwise we get string type 
        for i in range(20):
            await self.send_json({
                "message": str(i)
            })
            await asyncio.sleep(1)
        
    async def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)
        
    