'''
Created on May 21, 2017

@author: acer
'''
cfg={'active':['Flying-A320s','meetup','github','bitcoin','Bart','twitter'] #['Flying-A320s','meetup','github','bitcoin']
     ,'chDetails': {
         'bitcoin':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bitcoin-transactions"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Bitcoin msgs in last 5 mins"}}
         }
         ,'meetup':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"Meetup-RSVP"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Meetup msgs in last 5 mins"}}     
         }
         ,'github':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"github-events"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Github events in last 5 mins"}}     
         }
         ,'Flying-A320s':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"air-traffic"
                         ,"filter":'select * where aircraft = "A320" and speed>200'
                                                    }},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"A320 air-traffic events in last 5 mins"}}     
         }
         ,'Bart':{'pDu':{
                "action":"rtm/subscribe","id":"20","body":{"channel":"bartarrivalsschedule"}},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"BART events in last 5 mins"}}     
         }
        ,'twitter':{'pDu':{
                "action":"rtm/subscribe","id":"20"
                ,"body":{"channel":"Twitter-statuses-sample"
                                                    }},'classNM':'default.default',
                "charts":{"msgRate":{"Title":"Twitter sensitive events in last 5 mins"}}     
         }
                                
    }
     ,'engines':{} #placeholder to store the processing engines (created from classNM) during run
     ,'settings':{'refreshInterval':6000}
}
if __name__ == '__main__':
    pass