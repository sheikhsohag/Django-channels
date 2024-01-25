from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from time import sleep
import asyncio

class MyWebsocketConsumer(WebsocketConsumer):
    
    def connect(self):
        print("Websocket Connected...")
        self.accept()
        # self.close() #To reject the connection
        
    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client...', text_data)
        
        for i in range(10):
            self.send(text_data=str(i))
            sleep(1)
        # self.send(text_data="Messages from server to Client ")
        
        # self.send(bytes_data=data)  #To send binary frame to client
        # self.close(code = 4123)    #errors code
    
    def disconnect(self, close_code):
        print('Disconnected...', close_code)
        
        
class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("AsyncWebsocketConsumer Connected...")
        await self.accept()
        # self.close() #To reject the connection
        
    async def receive(self, text_data=None, bytes_data=None):
        print('AsyncWebsocketConsumer Message Received from Client...', text_data)
        for i in range(10):
            await self.send(text_data=str(i))
            await asyncio.sleep(1)
        
        # self.send(bytes_data=data)  #To send binary frame to client
        # self.close(code = 4123)    #errors code
    
    async def disconnect(self, close_code):
        print('AsyncWebsocketConsumer Disconnected...', close_code)