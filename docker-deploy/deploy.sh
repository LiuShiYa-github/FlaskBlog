#!/usr/bin/env bash
# git clone https://github.com/LiuShiYa-github/FlaskBlog.git
# cd FlaskBlog/docker-deploy
wget http://nginx.org/download/nginx-1.18.0.tar.gz
docker build -t  flaskblog:v1.0  ./
docker run -d -it --network host --name flaskblog flaskblog:v1.0 bash