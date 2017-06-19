import asyncio
import websockets
import json
from src.satori.channels.ch import ch
import threading
import logging

class readWebsock ():
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
    async def hello(self):
        #urlString = endpoint + '?appkey='+appkey
        myCh=ch(self.chNM,self.maxMsgCount)
        print (myCh.urlString)
        
        async with websockets.connect(myCh.urlString) as websocket:
            await websocket.send(json.dumps(myCh.pDu))
            print("> {}".format(myCh.pDu))
    
            greeting = await websocket.recv()
            print("< {}".format(greeting))
            while True:
                message = await websocket.recv()
                #print (message)
                myCh.showMessage(message)
                if myCh.stopCondition():
                    break
if __name__ == '__main__':
    rws=readWebsock('bitcoin',1)
    asyncio.get_event_loop().run_until_complete(rws.hello())
print("Ended")