from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer



class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        print('websocket Connetcted...')
        self.accept()
        # self.close()   #to reject the connections
        
        
    def receive_json(self, content, **kwargs):
        print('Message received from client....', content)
        # this content is dict formmat because of used jsonWebsocketconsumer..
        # otherwise we get string type 
        print('Type of content...', type(content))
        
        self.send_json({'msg':'message from server to client'})
        
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
        print('Type of content...', type(content))
        
        await self.send_json({'msg':'message from server to client'})
        
    async def disconnect(self, close_code):
        print('Websocket Disconnected...', close_code)
        
    