import asyncio
import websockets
import json
from src.satori.channels.ch import ch
import logging
import sys
log = logging.getLogger(__name__)

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
    async def customError(self):
        await asyncio.sleep(1)
        raise ValueError('A very specific bad thing happened')
        return "woke up!"
        
    async def hello(self):
        #urlString = endpoint + '?appkey='+appkey
        myCh=ch(self.chNM,self.maxMsgCount)
        log.info('Connect to : ' + myCh.urlString)
        while True:
            async with websockets.connect(myCh.urlString) as websocket:
                await websocket.send(json.dumps(myCh.pDu))
                print("> {}".format(myCh.pDu))
        
                greeting = await websocket.recv()
                if (json.loads(greeting)['action'] != 'rtm/subscribe/ok'):
                    log.info("< {}".format(greeting))
                    log.info(json.dumps(myCh.pDu))
                    return #stop reading this channel
                print("< {}".format(greeting))
                while True:
#                     try:
#                         message = await self.customError()
#                         print (message)
#                     except Exception as e:
#                         print ("Caught exception!" + str(e))
#                         break
                    try:
                        message = await websocket.recv()
                        #print (message)
                        myCh.showMessage(message)
                        if myCh.stopCondition():
                            return
                    except Exception as e:
                        log.info("Caught exception!" + str(e))
                        break
        #loops eternally --> in case of read error, connects again.
if __name__ == '__main__':
    print("Running as main only for test! ")
    rws=readWebsock('bitcoin',1)
    asyncio.get_event_loop().run_until_complete(rws.hello())
print("Ended")