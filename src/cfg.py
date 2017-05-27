'''
Created on May 21, 2017

@author: acer
'''
cfg={'active':['exchange','Flying-A320s','meetup','github'] #['Flying-A320s','meetup','github','bitcoin','Bart','twitter'] #
     ,'settings':{'refreshInterval':6000,'noOfMsgs':10000,'slotShiftTimeSecs':10,'totalRunTime':300}
     ,'chDetails': {
         'bitcoin':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bitcoin-transactions"}},'classNM':'bitcoin.bitcoin',
                "charts":{"msgRate":{
                    "mixin":{"Title":"Bitcoin msgs 10 second msg count"}}}
         }
         ,'meetup':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"Meetup-RSVP"}},'classNM':'default.default',
                "charts":{"msgRate":{
                    "mixin":{"Title":"Meetup msgs 10 second msg count"}}}  
         }
         ,'github':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"github-events"}},'classNM':'default.default',
                "charts":{"msgRate":{
                    "mixin":{"Title":"Github events 10 second msg count"}}}    
         }
         ,'Flying-A320s':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"air-traffic"
                         ,"filter":'select * where aircraft = "A320" and speed>200'
                                                    }},'classNM':'default.default',
                "charts":{"msgRate":{
                    "mixin":{"Title":"A320 air-traffic events 10 second msg count"}}} 
         }
         ,'Bart':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bartarrivalsschedule"}},'classNM':'default.default',
                "charts":{"msgRate":{
                    "mixin":{"Title":"BART events 10 second msg count"}}}   
         }
        ,'twitter':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"Twitter-statuses-sample"}},'classNM':'default.default',
                "charts":{"msgRate":{
                    "mixin":{"Title":"Twitter events 10 second msg count"}}}     
         }
        ,'exchange':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"exchange-rates"
                                                    }},'classNM':'bitcoin.exchange',
                "charts":{"msgRate":{
                    "mixin":{"Title":"Dollar exchange rate updated every 30 seconds","chartType":'column',"haxis_title":"rate/$"}}}   
         }                             
    }
     ,'websocketDetails': {
         'endpoint':"wss://open-data.api.satori.com", 'appkey':"E0Acebca1fbB549AaBeA5D9bec2aacb8"
        #urlString = endpoint + '?appkey='+appkey
    }
     ,'engines':{} #placeholder to store the processing engines (created from classNM) during run
}
if __name__ == '__main__':
    pass