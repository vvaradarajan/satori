from flask import Flask,get_template_attribute,send_from_directory
from src.satori.websock import readWebsock
#from src.satori.bitcoin2Old import meetup
from src.satori.channels.ch import ch, timerForSlotShift
import json
import markdown
from pprint import pprint
from src.cfg import cfg
import os
app = Flask(__name__,static_url_path='/static')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
 
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
    if setting=='all':
        js=cfg['settings']
        js['noOfPanelCharts']=len(cfg['active'])
        chartTypes=[]
        for c in cfg['active']:
            if 'chartType' in cfg['chDetails'][c]['charts']:
                chartTypes.append(cfg['chDetails'][c]['charts']['chartType'])
            else:
                chartTypes.append('bar')
        js['chartTypes']=chartTypes
        return json.dumps(js)
        
    if setting == 'noOfPanelCharts':
        return str(len(cfg['active']))
    return "0"

@app.route('/satori/<path:menuItem>')
def send_satori(menuItem):
    if menuItem=='Chart':
        chNM=cfg['active'][0]
        chartClass=cfg['engines'][chNM]
        pprint(chartClass.slots.getSlotsJson(chNM))
        return json.dumps(chartClass.slots.getSlotsJson(chNM))
    print('menuItem is: '+menuItem)
    if menuItem=='ChartPanel':
        chartDataArr=[]
        pprint(cfg['engines'])
        for chNM in cfg['active']:
            chartDataArr.append(cfg['engines'][chNM].getSlotsJson(chNM))
        return json.dumps(chartDataArr)

    if menuItem=='Algorithm':
        md=None
        with open(os.path.join(APP_STATIC, 'Algorithm.md')) as f:
            md = f.read()
        extensions = ['extra', 'smarty']
        html = markdown.markdown(md, extensions=extensions, output_format='html5')
        defMsg={}
        defMsg['Message']=html
        return json.dumps(defMsg)
            
        #return '[["Time", "count"], ["0", 5], ["1", 6], ["2", 7]]'
    #All others return a default message
    defMsg={}
    defMsg['Message']='Content development in Progress for {0}.  Try ChartPanel instead..'.format(menuItem)
    return json.dumps(defMsg)


if __name__ == "__main__":
    #ch.loadChClassesInCfg()
    rwsArr=[]
    for chNM in cfg['active']:
        rws=readWebsock(chNM,cfg['settings']['noOfMsgs'])
        rwsArr.append(rws)
        rws.start()
    # start timer
    tss=timerForSlotShift(cfg['settings']['slotShiftTimeSecs'],cfg['settings']['totalRunTime']) # start the timer thread
    tss.start()
    
    app.run(host='0.0.0.0') #0.0.0.0 allows external connections .. otherwise flash restricts it to localhost