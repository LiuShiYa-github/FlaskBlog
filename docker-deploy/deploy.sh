#!/usr/bin/env bash
cd ../../ && mv FlaskBlog/docker-deploy/* .
wget http://nginx.org/download/nginx-1.18.0.tar.gz
chmod +x init.sh
docker build -t  flaskblog:v1.0  ./
docker network create --subnet=172.32.0.0/24 flaskblog_net
docker-compose -f docker-compose.yaml up -d >>/dev/null 2>&1
sleep 3
docker exec -it mysql mysql -uroot -p123456 -e "use mysql; update user set host='%' where user ='root'; FLUSH PRIVILEGES; create database flaskdb;"
docker exec -it flaskblog flask createsuperuser --username admin --password admin