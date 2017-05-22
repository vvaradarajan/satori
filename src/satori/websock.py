import asyncio
import websockets
import json
from src.satori.channels.ch import ch
import threading

class readWebsock (threading.Thread):
# #channel = "bitcoin-transactions"
# channel = "Meetup-RSVP"
# #channel = "bitcoin-transactions"
# #channel = "bitcoin-transactions"    
# 
# endpoint = "wss://open-data.api.satori.com"
# 
# appkey = "E0Acebca1fbB549AaBeA5D9bec2aacb8"
    def __init__(self,chNM,maxMsgCount):
        super().__init__()
        self.chNM=chNM #name of the channel (defined in bitcoin2.ch)
        self.maxMsgCount=maxMsgCount
    async def hello(self,ch):
        #urlString = endpoint + '?appkey='+appkey
        print (ch.urlString)
        async with websockets.connect(ch.urlString) as websocket:
            await websocket.send(json.dumps(ch.pDu))
            print("> {}".format(ch.pDu))
    
            greeting = await websocket.recv()
            print("< {}".format(greeting))
            while True:
                message = await websocket.recv()
                #print (message)
                ch.showMessage(message)
                if ch.stopCondition():
                    break
    def run(self):
        bt=ch(self.chNM,self.maxMsgCount)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.hello(bt))
if __name__ == '__main__':
    rws=readWebsock('bitcoin',1)
    rws.start()
    rws1=readWebsock('bitcoin',1)
    rws1.start()
    rws.join()
    rws1.join()
print("Ended")