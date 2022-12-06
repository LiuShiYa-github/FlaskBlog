# 过程
# git clone https://github.com/LiuShiYa-github/FlaskBlog.git
# touch Dockerfile
# wget http://nginx.org/download/nginx-1.18.0.tar.gz
# vim nginx.conf
# vim init.sh
# docker build -t  flaskblog:v1.0  ./

# version: 1.0
FROM python:latest
ADD nginx-1.18.0.tar.gz /nginx/
ADD ../../FlaskBlog/ /nginx/
ADD init.sh /nginx/
WORKDIR /nginx/
RUN useradd nginx -M -s /sbin/nologin
RUN ./configure  --prefix=/etc/nginx/ --sbin-path=/usr/local/bin/ --user=nginx --group=nginx   --with-http_ssl_module  --with-http_stub_status_module --conf-path=/etc/nginx/nginx.conf  --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid
RUN make
RUN make install
RUN pip install uwsgi
RUN pip install -r requirements.txt
ADD nginx.conf /etc/nginx/
CMD ["/bin/bash","init.sh"]
EXPOSE 80