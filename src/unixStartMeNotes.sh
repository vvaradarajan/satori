#!/usr/bin/env bash
cd ~/satori
export PYTHONPATH=.
## nohup python3.6 src/chToRedisAsync.py &  OR nohup python3.6 src/chToRedis.py=> start the redis feeder
#### start the runMe.py webserver
## uwsgi has been install as a system service (systemd) as satori
## sudo service satori start #start the uwsgi
#### start the redis
## Also make sure that redis is running (nohup redis-server &)
#### start the nginx
## nginx -s reload => use if changes made to ngins config.

#### stop allall ####
## nginx -s reload => use if changes made to ngins config.
## kill -s SIGQUIT <all uwsgi pids) => quit old uwsgi (Note: uwsgi automatically runs Python app
## nohup uwsgi --ini ./src/satori_uwsgi.ini & => starts uwsgi (and that starts the python/flask app server)

##

#########Running instruction on local ##############
1. From Eclipse: run the runMe.py
2. From the command prompt: 
   cd C:\vasan\workspaceDecisions\satori1 (where project is)
   set PYTHONPATH=.
   python src/chToRedis.py (Keep this running)

#########Two modes of running ############
Using Threading (chToRedis.py, websock.py)
Using asyncio (chToRedisAsync.py, websockAsync.py)
The asyncio is simpler!