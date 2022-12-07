#!/usr/bin/env bash
# 启动nginx
nginx
# 创建数据库
msyql -uroot -p123456 -e "create database flaskdb"
# 创建表
flask db init
flask db migrate
flask db upgrade
# 创建初始化管理员
flask createsuperuser --username admin --password admin
# 启动uwsgi
nohup uwsgi config.ini &