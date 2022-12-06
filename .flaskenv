[uwsgi]
socket = 127.0.0.1:8080
home = /usr/local
wsgi-file = ./manage.py
callable=app
processes = 1
threads = 1
buffer-size = 32768
master = true
stats=./uwsgi.status
pidfile=./uwsgi.pid
