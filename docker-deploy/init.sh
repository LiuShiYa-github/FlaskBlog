#!/usr/bin/env bash
# 创建表
flask db init
flask db migrate
flask db upgrade
# 启动uwsgi
nohup uwsgi config.ini &
# 启动nginx
nginx