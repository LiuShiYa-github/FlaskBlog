#!/usr/bin/env bash
cd ../../ && mv FlaskBlog/docker-deploy/* .
wget http://nginx.org/download/nginx-1.18.0.tar.gz
chmod +x init.sh
docker build -t  flaskblog:v1.0  ./
docker network create --subnet=172.32.0.0/24 flaskblog_net
docker-compose -f docker-compose_mysql.yaml up -d
sleep 20
docker exec -it mysql mysql -uroot -p123456 -e "use mysql; GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' ; flush privileges; create database flaskdb;"
docker-compose -f docker-compose_flaskblog.yaml up -d
sleep 3
docker exec -it flaskblog flask createsuperuser --username admin --password admin
