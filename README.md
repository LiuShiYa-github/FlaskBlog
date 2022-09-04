# 作者的笔记

```text
http://www.lotdoc.cn/blog/topic/detail/6/
```

#作者的演示站

```text
http://flask.proae.cn/
```

#作者gitee

```text
https://gitee.com/qbiancheng
```

# 官方文档

```text
https://flask.palletsprojects.com/en/2.2.x/
```

# 容器方式启动mysql5.7
```bash
# ①下载docker-compose
curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# ②粘贴docker-compose.yaml
version: '3'
services:
  mysql:
    image: 'mysql/mysql-server:5.7'
    restart: always
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: 123456
    command:
      --default-authentication-plugin=mysql_native_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --explicit_defaults_for_timestamp=true
      --lower_case_table_names=1
      --max_allowed_packet=128M;
    ports:
      - 3306:3306
# ③启动MySQL并授权远程用户登录
docker-compose -f docker-compose.yaml up -d
docker exec -it  mysql bash
mysql -uroot -p123456
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```


# 方式一：SQLAlchemy控制台操作数据库同步

```text
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
flask.exe shell
>>> from RealProject import db
>>> db.create_all()
```

# 方式二：Flask-Migration控制台操作数据库同步

```text
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
flask.exe db init
flask.exe db migrate
flask.exe db upgrade
```

# 本项目前端依赖的第三方框架有：

```text
buefy -- https://buefy.org/
bulma -- https://bulma.io/
vue2 -- https://v2.cn.vuejs.org/v2/guide/
图标 -- https://materialdesignicons.com/
```


# 问题

```text
## 级联删除的定义？作用？使用场景？ 其他的处理方式？
## 后端的视图如何与前端html进行交互的？
## 前端页面怎么写？
## 设计数据库表单时如何处理一对多和多对多的关系？
## wtforms 表单函数的使用
```


# 实现过程中遇到的问题

```text
## Flask 表单form.validate_on_submit()总是false
https://blog.csdn.net/six66667/article/details/85885583
```
