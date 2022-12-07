#!/usr/bin/env bash
# 启动nginx
nginx
# 创建表
flask db init
flask db migrate
flask db upgrade
# 启动uwsgi
nohup uwsgi config.ini &