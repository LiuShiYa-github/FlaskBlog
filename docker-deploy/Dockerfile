FROM python:latest
ADD nginx-1.18.0.tar.gz /
RUN mv /nginx-1.18.0 /nginx
ADD FlaskBlog/ /nginx/
ADD init.sh /nginx/
WORKDIR /nginx/
RUN useradd nginx -M -s /sbin/nologin \
    && ./configure  --prefix=/etc/nginx/ --sbin-path=/usr/local/bin/ --user=nginx --group=nginx   --with-http_ssl_module  --with-http_stub_status_module --conf-path=/etc/nginx/nginx.conf  \
    --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid  \
    && make && make install && pip install uwsgi && pip install -r requirements.txt && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ADD nginx.conf /etc/nginx/
ADD config.ini /nginx/
CMD ["/bin/bash","init.sh"]
EXPOSE 80