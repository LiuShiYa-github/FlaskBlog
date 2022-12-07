#!/usr/bin/env bash
function deploy() {
    mv FlaskBlog/docker-deploy/* .
    wget http://nginx.org/download/nginx-1.18.0.tar.gz
    chmod +x init.sh
    docker build -t  flaskblog:v1.0  ./
    docker network create --subnet=172.32.0.0/24 flaskblog_net
    docker-compose -f docker-compose_mysql.yaml up -d
    while [ 0 -eq "$(docker ps -a|grep mysql|awk -F 'Up ' '{print $2}'|grep -c '2')" ]; do
      echo "Wait for the MySQL server to finish starting"
      sleep 3
    done
    docker exec -it mysql mysql -uroot -p123456 -e "use mysql; GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' ; flush privileges; create database flaskdb;"
    docker-compose -f docker-compose_flaskblog.yaml up -d
    docker exec -it flaskblog flask createsuperuser --username admin --password admin
}
function get_ip() {
    # shellcheck disable=SC2010
    network_name=$(ls /etc/sysconfig/network-scripts/ifcfg-*|grep -v lo|awk -F '/etc/sysconfig/network-scripts/ifcfg-' '{print $2}')
    network_ip=$(ifconfig "$network_name" | awk 'NR==2{print $2}')
    echo "Please use your browser to access http://$network_ip"
}
function main() {
    deploy
    get_ip
}
main
