#!/usr/bin/env bash
cd ../../ && mv FlaskBlog/docker-deploy/* .
wget http://nginx.org/download/nginx-1.18.0.tar.gz
chmod +x init.sh
docker build -t  flaskblog:v1.0  ./
