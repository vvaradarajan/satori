#!/usr/bin/env bash
cd ~/satori
export PYTHONPATH=.
#### uncomment the following commands as needed ####
## nginx -s reload => use if changes made to ngins config.
## kill -s SIGQUIT <all uwsgi pids) => quit old uwsgi (Note: uwsgi automatically runs Python app
## nohup uwsgi --ini ./src/satori_uwsgi.ini & => starts uwsgi (and that starts the python/flask app server)
## nohup python3.6 src/chToRedis.py & => start the redis feeder
## Also make sure that redis is running (nohup redis-server &)
