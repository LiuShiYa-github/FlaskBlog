#!/usr/bin/env bash
# 启动nginx
nginx
# 创建初始化管理员
flask createsuperuser --username admin3 --password admin3
# 启动uwsgi
nohup uwsgi config.ini &