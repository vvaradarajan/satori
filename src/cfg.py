'''
Created on May 21, 2017

@author: acer
'''
cfg={'active':['Flying-A320s','meetup','github','bitcoin','Bart','twitter'] #['Flying-A320s','meetup','github','bitcoin']
     ,'settings':{'refreshInterval':6000,'noOfMsgs':10000,'slotShiftTimeSecs':10,'totalRunTime':60}
     ,'chDetails': {
         'bitcoin':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bitcoin-transactions"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Bitcoin msgs 10 second msg count"}}
         }
         ,'meetup':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"Meetup-RSVP"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Meetup msgs 10 second msg count"}}     
         }
         ,'github':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"github-events"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Github events 10 second msg count"}}     
         }
         ,'Flying-A320s':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"air-traffic"
                         ,"filter":'select * where aircraft = "A320" and speed>200'
                                                    }},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"A320 air-traffic events 10 second msg count"}}     
         }
         ,'Bart':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bartarrivalsschedule"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"BART events 10 second msg count"}}     
         }
        ,'twitter':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"Twitter-statuses-sample"
                                                    }},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Twitter events 10 second msg count"}}     
         }
                                
    }
     ,'engines':{} #placeholder to store the processing engines (created from classNM) during run
}
if __name__ == '__main__':
    pass