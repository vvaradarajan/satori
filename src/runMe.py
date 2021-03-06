##### This file can be run by itself, and works without nginx, uwsgi (requires redis) ####
##### Note: the program chToRedis.py MUST be running in the background #####
##Normal commands to run using nginx and uwsgi:
## Do all this from satori directory
## export PYTHONPATH=.
## nginx -s reload => use if changes made to ngins config.
## kill -s SIGQUIT <all uwsgi pids) => quit old uwsgi (Note: uwsgi automatically runs Python app
## nohup uwsgi --ini ./src/satori_uwsgi.ini & => starts uwsgi (and that starts the python/flask app server)
## nohup python3.6 src/chToRedis.py & => start the redis feeder
## Also make sure that redis is running (nohup redis-server &)
from flask import Flask,get_template_attribute,send_from_directory
#from src.satori.websock import readWebsock
#from src.satori.bitcoin2Old import meetup
#from src.satori.channels.ch import ch, timerForSlotShift
import json
import markdown
from pprint import pprint
from src.cfg_satori import cfg_satori
from src.cfg_math import cfg_math
from src.cfg_power import cfg_power
import os
import redis
import logging
class myFlask(Flask):
    def __init__(self,nM,**kwargs):
        #start the threads for websocket read and timer
#         rwsArr=[]
#         for chNM in cfg['active']:
#             rws=readWebsock(chNM,cfg['settings']['noOfMsgs'])
#             rwsArr.append(rws)
#             rws.start()
#         # start timer
#         tss=timerForSlotShift(cfg['settings']['slotShiftTimeSecs'],cfg['settings']['totalRunTime']) # start the timer thread
#         tss.start()
        super(myFlask, self).__init__(nM,**kwargs)
        
app = myFlask(__name__,static_url_path='/static')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
redisMem = redis.Redis(host='localhost', port=6379, db=0)
APP_ROLE='power'
cfg = eval('cfg_'+APP_ROLE)
@app.route("/a")
def hello():
    return "Hello World!"

@app.route("/template") 
def helloTpt():
    hello = get_template_attribute('hellotemplate.txt', 'hello')
    return hello('World')

@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory('../bower_components', path)
@app.route('/my_components/<path:path>')
def send_my_components(path):
    return send_from_directory('my_components', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('../images', path)

@app.route('/settings/<path:setting>')
def send_settingsData(setting):
    if setting=='satori':
        js=cfg['settings']
        js['noOfPanelCharts']=len(cfg['active'])
        chartMixins=[]
        for c in cfg['active']:
            mixin=cfg['chDetails'][c]['charts']['msgRate']['mixin']
            mixin['id']=c
            chartMixins.append(mixin)
        js['chartMixins']=chartMixins
        return json.dumps(js)
    if setting=='power':
        #The settings comes from the config. (General seperation of web-server from subject code)
        return redisMem.get('settings').decode('utf-8')
    if setting=='math':
        js=cfg_math['settings'];
        return json.dumps(js)
    if setting == 'noOfPanelCharts':
        return str(len(cfg_satori['active']))
    return "0"

@app.route('/satori/<path:menuItem>')
def send_satori(menuItem):
    print('menuItem is: '+menuItem)
    if menuItem=='Chart':
        chNM=cfg['active'][0]
        chartClass=cfg['engines'][chNM]
        pprint(chartClass.slots.getSlotsJson(chNM))
        return json.dumps(chartClass.slots.getSlotsJson(chNM))
    elif menuItem=='ChartPanel':
        #return the data from redis
        return(str(redisMem.get('chartPanel'),'utf-8'))


    elif menuItem in ['Algorithm','Blog','PowerBattery']:
        if (menuItem=='Algorithm'):
            fileNM='Algorithm.md'
        else:
            if (menuItem=='PowerBattery'):
                fileNM='PowerBatteryOptimization.md'
            else:
                fileNM='DataStructureForFullStack.md'
        md=None
        with open(os.path.join(APP_STATIC, fileNM)) as f:
            md = f.read()
        extensions = ['extra', 'smarty','tables']
        html = markdown.markdown(md, extensions=extensions, output_format='html5')
        defMsg={}
        defMsg['Message']=html
        return json.dumps(defMsg)
    elif menuItem == 'ReloadData':
        redisMem.set('reloadData','T')
        return "Data Loaded"
        #return '[["Time", "count"], ["0", 5], ["1", 6], ["2", 7]]'
    #All others return a default message
    else:
        defMsg={}
        defMsg['Message']='Content development in Progress for {0}.  Try ChartPanel instead..'.format(menuItem)
        return json.dumps(defMsg)

if __name__ == "__main__":
    #ch.loadChClassesInCfg()   
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger(__name__)
    log.info("Starting Satori WebServer")
    app.run(host='0.0.0.0') #0.0.0.0 allows external connections .. otherwise flash restricts it to localhost