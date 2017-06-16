#!/usr/bin/env bash
cd ~/satori
export PYTHONPATH=.
#### uncomment the following commands as needed ####
## nginx -s reload => use if changes made to ngins config.
## kill -s SIGQUIT <all uwsgi pids) => quit old uwsgi (Note: uwsgi automatically runs Python app
## nohup uwsgi --ini ./src/satori_uwsgi.ini & => starts uwsgi (and that starts the python/flask app server)
## nohup python3.6 src/chToRedis.py & => start the redis feeder
## Also make sure that redis is running (nohup redis-server &)
## uwsgi has been install as a system service (systemd)
## sudo service satori start
##

#########Running instruction on local ##############
1. From Eclipse: run the runMe.py
2. From the command prompt: 
   cd C:\vasan\workspaceDecisions\satori1 (where project is)
   set PYTHONPATH=.
   python src/chToRedis.py (Keep this running)
