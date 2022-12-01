本文档是在跟随B站up主轻编程学习flask开发的基础上增加了部分功能并整理的笔记。

# 技术栈以及工具

```text
python 3.10
flask 2.1 版 - https://flask.palletsprojects.com/en/2.1.x/
bulma css框架 - https://bulma.io/
mysql8.0
prcharm
作者文档：http://www.lotdoc.cn/blog/detail/183/?menu=6
```

# 环境准备

容器方式启动mysql5.7
```text
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


```text
# 创建虚拟环境
> mkdir FlaskBlog
> cd FlaskBlog
> python -m venv venv
# 激活虚拟环境
venv\Scripts\activate

$ E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install flask

PS E:\pythonproject\FlaskBlog> E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install flask
Requirement already satisfied: flask in e:\pythonproject\flaskblog\venv\lib\site-packages (2.2.2)
Requirement already satisfied: Jinja2>=3.0 in e:\pythonproject\flaskblog\venv\lib\site-packages (from flask) (3.1.2)
Requirement already satisfied: click>=8.0 in e:\pythonproject\flaskblog\venv\lib\site-packages (from flask) (8.1.3)
Requirement already satisfied: importlib-metadata>=3.6.0 in e:\pythonproject\flaskblog\venv\lib\site-packages (from flask) (4.12.0)
Requirement already satisfied: itsdangerous>=2.0 in e:\pythonproject\flaskblog\venv\lib\site-packages (from flask) (2.1.2)
Requirement already satisfied: Werkzeug>=2.2.2 in e:\pythonproject\flaskblog\venv\lib\site-packages (from flask) (2.2.2)
Requirement already satisfied: colorama in e:\pythonproject\flaskblog\venv\lib\site-packages (from click>=8.0->flask) (0.4.5)
Requirement already satisfied: zipp>=0.5 in e:\pythonproject\flaskblog\venv\lib\site-packages (from importlib-metadata>=3.6.0->flask) (3.8.1)
Requirement already satisfied: MarkupSafe>=2.0 in e:\pythonproject\flaskblog\venv\lib\site-packages (from Jinja2>=3.0->flask) (2.1.1)
WARNING: You are using pip version 21.3.1; however, version 22.3.1 is available.
You should consider upgrading via the 'E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install --upgrade pip' command.

=========================================================================

在安装flask的同时也自动安装了Werkzeug/Jinja/MarkupSafe/ItsDangerous/Click五个依赖！
1、ItsDangerous安全地对数据进行签名，以确保其完整性。这用于保护 Flask 的会话 Cookie。
2、Click 是用于编写命令行应用程序的框架。它提供命令并允许添加自定义管理命令。
3、Jinja 是一种模板语言，用于呈现应用程序所服务的页面。
4、Werkzeug实现了WSGI，这是应用程序和服务器之间的标准Python接口。
5、MarkupSafe附带了Jinja。它在呈现模板时转义不受信任的输入，以避免注入攻击。
```

# 快速上手

首先创建一个app.py的文件，以开始我们下来的操作

## 新增app.py文件并创建试图

```python
from flask import Flask  # 导入flask类

app = Flask(__name__)  # flask实例化


@app.route("/")  # route装饰器，告诉Flask哪个URL应该触发我们的函数
def hello_world():  # 视图函数
    return "<p>Hello, World!</p>"

```

## 运行项目

在终端运行flask run命令，将启动flask自带的开发服务器，终端输出如下所示：

```text
PS E:\pythonproject\FlaskBlog> E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [13/Nov/2022 10:23:18] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [13/Nov/2022 10:23:18] "GET /favicon.ico HTTP/1.1" 404 -

```
![img.png](img.png)


# 目录结构规划
## 目录结构

为保证项目可持续发展，利于后期扩展，我们从开始创建项目就应该先规划好目录结构，一个好的目录结构可以让我们的项目整洁有序，并利于维护和后期进一步扩展!
之前快速上手中创建的app.py的文件便可以删除，亦或者你重新创建一个项目开始以下的内容，建议是新建一个目录来开始我们以下的内容！

## 创建应用目录(app)

在实际开发过程中，一个完整的项目一定是由多个不同的功能模块构成，以我们的博客系统为例，主要由两个大的功能模块构成，一个是负责用户认证以及用户权限操作的模块auth, 一个则是我们博客的主应用模块blog，他主要负责博客的内容/分类等一些与博客相关的功能！
为了实现以上需求，我们就需要现在虚拟环境venv的同级目录新建一个app的目录，用这个目录来统一管理各功能模块，并在其内部分别新建auth和blog目录,结构如下所示！

![img_1.png](img_1.png)

## 创建项目目录

为了区别app目录和RealProject目录，我们将分别称起名为 应用目录（app），项目目录（RealProject），
在app的同级我们创建一个RealProject的目录，并分别在其内部创建__init__.py、settings.py、wsgi.py三个文件, 目录结构如下：
![img_2.png](img_2.png)


## 创建入口文件

最后，我们将创建一个manage.py入口文件作为我们整个项目的入口，最后我们只需要运行该文件即可启动我们的项目！

# 工厂函数

```text
无论是一个单文件项目还是一个多功能模块的大型项目，我们始终应该明白，Flask 应用程序是 Flask 类的一个实例。基于此，那么第一件事就是实例化一个Flask对象！
创建 Flask 应用程序最直接的方法是直接在代码顶部创建一个全局 Flask 实例，就像我们快速上手中的那样！
在大型项目中这种做法是行不通的，而是在一个函数内创建它。此函数被称为应用程序工厂，简称-工厂函数。应用程序所需的任何配置、注册和其他设置都将在函数内部进行，然后应用程序将被返回。
```

在项目目录(RealProject)目录下的__init__.py中创建如下代码：

```python
import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    ## instance_relative_config设置为True则代表开启从文件加载配置，默认为False
    app = Flask(__name__, instance_relative_config=True)
    # app.config其实调用的是flask类的config属性，该属性又被设置为了一个Config的类
    ## from_mapping则是该Config类下的一个方法，用来更新默认配置，返回值为True
    ## 至于Flask的默认配置项都有哪些，其实可以深入源码查看default_config属性所列出的项
    # 默认配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        # 如果没有传入，则从py文件加载配置，silent=True代表文件，文件加载成功则返回True
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)

    # 递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/")  # route装饰器，告诉Flask哪个URL应该触发我们的函数
    def hello_world():  # 视图函数
        return "<p>Hello, World!</p>"
    
    return app

```
(快速上手阶段的app.py就可以删除了)


在FlaskBlog目录下的manage.py中创建如下代码：

```text
from RealProject import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=80, debug=True)

```

# 蓝图应用Blueprint

```text
官方的解释，蓝图是一个对象，它允许在不需要应用程序对象的情况下定义应用程序函数。它使用与 Flask 相同的装饰器，但通过记录它们以供以后注册来推迟对应用程序的需求。
这段话该如何理解呢？其实这个没必要去深究，我们只要知道蓝图就是把我们应用目录的模块注册到Flask类，充当一个中间人的角色！
```

## 创建蓝图
学过django的同学应该知道，应用的视图函数一般都写在应用目录下的views.py中，没学过django也无关紧要，在应用目录app下的blog文件夹下创建一个views的软件包并在软件包下创建blog.py， 这里用来集中存储blog的视图代码！
通过蓝图创建一个博客首页的基本视图,代码如下：

```python
from flask import Blueprint

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('index/')
def index():
    return 'Hello Word'

```
(将RealProject目录录下的__init__.py中的试图函数可以删除掉了)

1、在app下blog目录的__init__.py中增加以下代码

```text
from .views import bp
```

2、在RealProject下的__init__.py的create_app中增加以下代码

```text
    # 引入blog的视图文件
    from app.blog.views import blog
    app.register_blueprint(blog.bp)
```
做完以上两步之后运行项目

![img_3.png](img_3.png)

## 代码详解
1、首先引入了蓝图对象，这个Blueprint与Flask类
```text
from flask import Blueprint
```
2、实例化一个蓝图对象，需要两个必须参数，第一个是应用的名称，第二个__name__是该应用的位置，其他参数都是可选的，我们这里用关键字参数url_prefix='/blog'指定了 该应用的一个url的命名空间，和django的urls中的app_name类似，这个值会出现在该应用url之前，比如我们现在这个url访问的话应该是：http://127.0.0.1/blog/index/
```text
bp = Blueprint('blog', __name__, url_prefix='/blog')
```
3、创建了blog应用的一个视图，用蓝图实例来绑定route，把该url定义在该应用当中
```text
@bp.route('index/')
def index():
    return render_template()
```
## 注册蓝图
上边我们都说了，这个应用通过蓝图创建，如果不去主项目注册的话，他是不会被运行的，这就要我们去工厂函数中注册蓝图！
首先，把该views文件引入到blog的__init__.py中，以便后续调用！
```text
from .views import bp
```

最后，在项目目录的__init__.py中的工厂函数中通过app实例的提供的register_blueprint方法注册蓝图，代码如下：

```text
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    # ... 省略部分代码

    # 引入blog的视图文件
    from app.blog.views import blog
    app.register_blueprint(blog.bp)

    return app
```
## 定义程序入口
在入口文件manage.py中引入一下代码，代码非常简单，不做过多解释
```text
from RealProject import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=80, debug=True)

```

# 安装Flask-SQLAlchemy
```text
Flask-SQLAlchemy 是 Flask 的扩展，它为您的应用程序添加了对 SQLAlchemy 的支持。它旨在通过提供有用的默认值和额外的帮助程序来简化将 SQLAlchemy 与 Flask 结合使用，从而更轻松地完成常见任务。
这是官方的介绍，其实对于刚想写个简单博客的同学来说，这个东西说了等于没说，因为他不知道SQLAlchemy是什么？能干什么？所以自然对以上这段话就无从理解！
我这里简单说一下，无论是博客类网站还是更大的商城类网站，我们在页面上所看到的数据都是存储在数据库，那数据库主要分为关系型数据库和非关系型数据库，那么，如何把数据存储到数据库以及如何把数据库中的数据查询到页面，也就是所谓的增删改查操作，我们都要用到sql语法，当然这又是另外的一个知识点，学起来也是非常的繁琐复杂，那为了我们快速实现增删改查的目的，有大佬就创作了这样一个框架，使用了一种叫做《Object Relation Mapping》对象关系映射的技术，也就是我们所说的ORM，这个在django框架中是自带的，但与SQLAlchemy框架的用法及底层实现有一些区别。这个我们无需去过多关注，我只要知道SQLAlchemy的API提供了执行数据库CRUD操作的方法，因此我们不必在程序中编写复杂难懂的原始SQL语句，就可以达到增删改查的目的。
那么，Flask-SQLAlchemy是对SQLAlchemy的进一步封装，使得更加容易的在Flask项目中使用SQLAlchemy！
```

## 安装Flask-SQLAlchemy
```text
E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install Flask-SQLAlchemy
```
官方文档：https://flask-sqlalchemy.palletsprojects.com/en/2.x/

## 使用
1、在项目目录（RealProject）的__init__.py中引入SQLAlchemy
```text
# RealProject/__init__.py
from flask_sqlalchemy import SQLAlchemy
# 实例化SQLAlchemy对象
db = SQLAlchemy()
```
2、在工厂函数create_app中与app绑定关系
```text
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 绑定数据库
    db.init_app(app)

    ...省略部分代码

    return app
```
3、创建模型数据
这一节我们来先创建一个博客的分类模型数据来认识一下模型的创建
在app/blog/models.py中创建模型如下
```text
from datetime import datetime
from RealProject import db


class Category(db.Model):
    """分类模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间

    def __repr__(self):
        return '<Category %r>' % self.name

```
学习过django的同学有没有一股熟悉的味道，和django的创建模型是不是非常相似，只是一些语法上的不同！
我们一起来看下这些字段都做了什么？
* id 该模型的主键，类型为Integer，primary_key为True代表主键
* name 分类名称，String类型，可变字符类型，映射到数据库中是varchar类型.
* icon 分类图标，类型与name一致，区别是nullable=True,就是允许为空，即默认值是null
* add_date 创建时间，nullable=False不能为空，default=datetime.utcnow设置为当前时区时间
* pub_date 更新时间，主要关注下onupdate=datetime.utcnow,这个可以更新每次编辑时的时间保存
其他更多的类型，我们在以后用到的时候再去了解.

## 配置MySQL数据库
我们最开始已经说过了项目的默认配置在工厂函数中已经引入了,以下就是项目的默认配置
```text
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
```
但是，一般的做法是配置和代码是区别开的，我们现在要让他从文件中读取配置，所以就直接删除这句，或者注释掉即可，最开始引入是为了介绍Flask加载配置文件的几种方法！
现在我们把所有的配置项移动到项目目录的settings.py文件中，配置如下：
```text
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'l%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@10.0.0.30:3306/flaskdb'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
```
以上几项配置是链接数据库必须的配置，其中SQLALCHEMY_DATABASE_URI就是链接mysql数据库的url，第一个root是用户名，冒号后的root是密码，3306是mysql数据库默认的端口号，最后一个flaskdb则是数据库名
接下来修改我们的工厂函数如下所示：
```text
import os
from flask import Flask
from RealProject.settings import BASE_DIR
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    # instance_relative_config设置为True则代表开启从文件加载配置，默认为False
    app = Flask(__name__, instance_relative_config=True)

    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)
    # 绑定数据库
    db.init_app(app)
    # 递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    # 注册数据库模型
    from app.blog.models import blog
    
    return app
    
```
安装mysql包
```text
E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install mysqlclient
```
做完以上步骤，如果你的数据库没有问题的话，就已经可以连接到数据库了，但是字段此时还并没有同步到数据库，同步字段到数据库的方法是，进入Flask的shell环境，运行以下两个命令即可：
```text
>>> from RealProject import db
>>> db.create_all()
```
但是，要进入Flask的shell环境需要先在终端设置项目的环境变量，我这里以Windows系统和本项目为例:
CMD终端，运行如下命令，即可进入shell环境
```text
set FLASK_APP=RealProject
set FLASK_ENV=development
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe shell
```
Powershell终端， 运行如下命令，即可进入shell环境
```text
$env:FLASK_APP = "RealProject"
$env:FLASK_ENV = "development"
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe shell
```
![img_4.png](img_4.png)

但是，我们不采用这种方法去同步数据库，下一章我们将采用Flask的另外一个扩展Flask-Migrate来同步数据库，他可以进行数据库的版本控制，比如你数据库某些字段已经有了默认数据，他不会去清空重建，而是会进行新增操作，类似于django的makemigrations和migrate两个命令所做的事情！

# Flask-Migrate
```text
Flask-Migrate 是一个扩展,他是Alembic的进一步封装，以更好的适配Flask和Flask-SQLAlchemy 应用程序。 就实际的数据库迁移而言，所有内容都由Alembic处理，因此您可以获得完全相同的功能。
Alembic 是一款轻量型的数据库迁移工具，它与 SQLAlchemy 一起共同为 Python 提供数据库管理与迁移支持。
```
## 安装Flask-Migrate
```text
E:\pythonproject\FlaskBlog\venv\Scripts\python.exe -m pip install Flask-Migrate
```
## 配置Flask-Migrate
1、首先在工厂函数所在文件中引入
* 路径：RealProject/init.py
```text
from flask_migrate import Migrate
migrate = Migrate()
```
2、在工厂函数中注册, 最终
```text
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 省略部分代码...

    db.init_app(app)

    # 注册migrate
    migrate.init_app(app, db)

    # 省略部分代码...

    return app
    
```
最后，完整的工厂函数如下
```text
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from RealProject.settings import BASE_DIR
from flask_migrate import Migrate

migrate = Migrate()
# 实例化SQLAlchemy对象
db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)

    # 递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 绑定数据库
    db.init_app(app)
    # 注册migrate
    migrate.init_app(app, db)
    
    # 引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)

    # 注册数据库模型
    from app.blog import models

    return app

```
## 使用Flask-Migrate
在上一节最后我们说过，需要导出项目的环境变量，才能使用flask的命令，因此在执行以下操作之前，记得先导出环境变量哦！
在此之前，我们已经创建好了一个博客的分类模型，并且将模型数据已经在工厂函数中注册！
下来，我们就可以使用以下命令创建迁移存储库：
```text
$env:FLASK_APP = "RealProject"
$env:FLASK_ENV = "development"
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db init
```
这会将迁移文件夹添加到应用程序中。此时，你可以发现项目目录多了一个migrations的文件夹，下边的versions目录下的文件就是生成的数据库迁移文件！
然后，运行以下命令生成迁移
```text
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db migrate
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db upgrade
```

```text
做完这两步就完成了第一次的初始迁移操作，我们可以看数据库已经有了我们创建的模型字段！
之后，每次在新增和修改完模型数据之后，只需要执行以下两个命令即可
```

```text
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db migrate
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db upgrade
```
到这里，基本上我们的项目最基本的配置就已经做完了，后边章节我们将开始真正的业务编写，Flask因其自身的灵活性，大部分的东西都得依靠第三方，所以前期的项目配置以及文件夹结构每个人的理念不同，自然设计出来的结构也是不同的，所以这就非常考验python的基础和能力，因此上，再开始项目之前，我们队python的相关基础知识一定要掌握的比较扎实，做起来才可能会更加轻松！

# 模型创建
```text
在之前的章节中我们已经知道模型对应的其实就是数据库字段，通过这种方式创建数据库字段的方式主要依赖的是ORM系统，当然如果你对sql语法非常熟悉，完全可以不用ORM，但使用ORM的好处是有利于避免一些sql注入的风险，对sql不熟悉的同学比较友好，但略微会有性能损失，使用sql语句的话，如果你学的是一知半解，也容易写出一些性能不佳的语句，各有各的优点和不足，没有谁更好，具体眼看你自己的业务场景
```
## 数据库字段规划
```text
一个博客我们先从最简单的入手，博客分类、文章内容、文章标签，应该说拥有这三个基本的功能就算是一个非常简单的博客，那么我们就先从这三个功能入手，开始设计数据库字段！
```

## 字段设计
![img_5.png](img_5.png)

## 博客分类模型（Category）
| 字段       | 类型           | 是否允许为空 | 说明   |
|----------|--------------|--------|------|
| id       | int(11)      | 否      | 主键   |
| name     | varchar(128) | 否      | 分类名称 |
| icon     | varchar(128) | 是      | 分类图标 |
| add_date | datetime     | 否      | 添加时间 |
| pub_date | datetime     | 否      | 更新时间 |

## 文章模型（Post）
| 字段          | 类型                    | 是否允许为空 | 说明           |
|-------------|-----------------------|--------|--------------|
| id          | int(11)               | 否      | 主键           |
| title       | varchar(128)          | 否      | 文章标题         |
| desc        | varchar(200)          | 是      | 文章简介         |
| has_type    | enum('draft', 'show') | 否      | 文章类型（草稿, 发布） |
| category_id | int(11)               | 否      | 归属分类id       |
| content     | longtext              | 否      | 文章内容         |
| add_date    | datetime              | 否      | 添加时间         |
| pub_date    | datetime              | 否      | 更新时间         |

## 文章标签（Tag）
| 字段       | 类型           | 是否允许为空 | 说明   |
|----------|--------------|--------|------|
| id       | int(11)      | 否      | 主键   |
| name     | varchar(128) | 否      | 分类名称 |
| add_date | datetime     | 否      | 添加时间 |
| pub_date | datetime     | 否      | 更新时间 |
## 文章与文章标签多对多关系（tags）
| 字段      | 类型      | 是否允许为空 | 说明     |
|---------|---------|--------|--------|
| tag_id  | int(11) | 否      | 文章标签id |
| post_id | int(11) | 否      | 文章id   |

规划好以上模型的字段后，就是去编写对应的模型类，这里有一些关系需要搞清楚，文章分类与文章是一对多的关系，一个分类下可以有多篇文章，而文章内容与标签之间的关系则是多对多的关系，一个标签可以对应多篇文章，多篇文章也可以对应某一个标签！

## 博客模型类创建
在app/blog/models/blog.py文件中创建模型类，通过观察，我们发现每个模型都有一个相同的添加时间字段和更新时间字段，那么我们就可以把这两个字段提取到一个基类模型中，然后让所有的模型均继承这个基类模型即可，基类模型不会生成数据库字段，但继承他的模型会继承他里边的字段！

1、首先需要引入这些模块
```text
from datetime import datetime
from RealProject import db
from enum import IntEnum
from sqlalchemy.dialects.mysql import LONGTEXT
```

2、创建基类模型BaseModel
```text
class BaseModel(db.Model):
    # 基类模型
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now, )  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)  # 更新时间
```
3、创建分类模型Category
```text
class Category(BaseModel):
    """分类模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)

    post = db.relationship('Post', backref='category', lazy=True)
    # post = db.relationship('Post', back_populates="category", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Category %r>' % self.name
```
注意，db.relationship()函数用来创建关系，这是一个隐式字段，不会出现在数据库，但可以使用orm的查询语法查到所有关联的数据，外键字段还必须使用外键类来单独声明！


4、创建文章标签模型
```text
class Tag(BaseModel):
    """ 文章标签
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布
```

5、创建文章模型Post
```text
# 多对多关系帮助器表
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                )


class Post(BaseModel):
    """ 文章
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # 多对多关系
    tags = db.relationship('Tag', secondary=tags,
                           lazy='subquery', backref=db.backref('post', lazy=True))

    # category = db.relationship("Category", back_populates="post")

    def __repr__(self):
        return '<Post %r>' % self.title
        
```
category_id字段的创建，它使用了db.ForeignKey()类实例化来创建了这个外键字段，这个会出现在数据库！这就是创建一对多关系字段的方法！
tags多对多关系则根据官方文档的建议是需要额外定义用于该关系的帮助器表，不建议使用模型，而是使用实际表！至于更详细的一些用法，我们可以参考其官方文档说明！
* 官方文档：https://flask-sqlalchemy.palletsprojects.com/en/2.x/


创建完以上模型之后，就可以执行迁移命令，注意，别忘记设置环境变量！

## 操作数据库
```text
操作数据库
方式一：SQLAlchemy控制台操作数据库同步
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
flask.exe shell
>>> from RealProject import db
>>> db.create_all()

方式二：Flask-Migration控制台操作数据库同步
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db init
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db migrate
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db upgrade
```

![img_6.png](img_6.png)

# 掌握增删改查
既然我们选择了使用ORM框架，那就必须熟练掌握其提供的增删改查方法，在正式编写视图事前，本节内容我们先在shell环境中来了解和熟悉其增删改查的基础方法！
参考资料：https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
## 插入记录
这里我们以博客的分类为案例进行演示
1、首先设置环境变量，进入shell环境
至于如何导出环境变量请参考《安装并配置Flask-SQLAlchemy》章节，最后同步数据库字段相关内容！
2、运行如下命令进入shell环境
```text
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe shell
```
3、导入模型数据
```text
>>> from RealProject import db
>>> from app.blog.models import Category, Post
```
## 插入一条分类记录
```text
>>> cate = Category(name='分类一')
>>> db.session.add(cate)
>>> db.session.commit()
>>> cate
<Category '分类一'>
```
以上就是插入向数据库插入一条记录的基本思路：
* 1、实例化模型的python对象
* 2、将该实例化对象添加到回话 db.session.add(cate)
* 3、提交该会话 db.session.commit()

![img_7.png](img_7.png)

![img_8.png](img_8.png)

## 查询记录
在查询之前我们先多添加几条分类数据的记录
* 拓展，批量插入数据的几种方法：http://www.lotdoc.cn/blog/detail/178/

```text
>>> cates = ['分类二', '分类三', '分类四']
>>> for name in cates:
...     cate = Category(name=name)       
...     db.session.add(cate)
...     db.session.commit()
...
>>> Category.query.all()
[<Category '分类一'>, <Category '分类2'>, <Category '分类3'>, <Category '分类4'>]
```
查询最常用方法有：all()、first()、get()、filter()、order_by()
* 按分类名称检索
```text
>>> cate1 = Category.query.filter_by(name='分类一').first()
>>> cate1.id
1
>>> cate1.name
'分类一'
```
这里如果传入的分类名称不存在则返回None!
* 通过更复杂的表达式查询多个分类：
```text
>>> Category.query.filter(Category.name.endswith('分类')).all()
[]
>>> Category.query.filter(Category.name.endswith('分类一')).all() 
[<Category '分类一'>]
>>> Category.query.filter(Category.name.endswith('2')).all()      
[<Category '分类2'>]
>>> Category.query.filter(Category.name.startswith('分')).all()  
[<Category '分类一'>, <Category '分类2'>, <Category '分类3'>, <Category '分类4'>]
```
模糊匹配某一个字段，endswith从字段的最后一个字符开始匹配，startswith从第一个字符开始匹配
* 按某字段进行排序：
```text
>>> Category.query.order_by(Category.add_date).all()
[<Category '分类一'>, <Category '分类2'>, <Category '分类3'>, <Category '分类4'>]
>>> Category.query.order_by(-Category.add_date).all()
[<Category '分类2'>, <Category '分类3'>, <Category '分类4'>, <Category '分类一'>]
```
* 限制查询数量
```text
>>> Category.query.limit(1).all()
[<Category '分类一'>]
>>> Category.query.limit(2).all() 
[<Category '分类一'>, <Category '分类2'>]
>>> Category.query.limit(3).all() 
[<Category '分类一'>, <Category '分类2'>, <Category '分类3'>]
```
* 按住键查询
```text
>>> Category.query.get(1)
<Category '分类一'>
```
## 更新方法
```text
>>> cate_2 = Category.query.get(2)
>>> cate_2.name = '分类二new'
>>> db.session.commit()
```
## 删除记录
```text
>>> cate = Category.query.get(1)
>>> db.session.delete(cate)
>>> db.session.commit()
```
## 常用查询和过滤方法
| 过滤方法        | 说明                                |
|-------------|-----------------------------------|
| filter()    | 使用指定的规则过滤记录，返回新产生的查询对象            |
| filter_by() | 使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象 |
| order_by()  | 根据指定条件对记录进行排序，返回新产生的查询对象          |
| group_by()  | 根据指定条件对记录进行分组，返回新产生的查询对象          |

下面是一些常用的查询方法：

| 查询方法           | 说明                                      |
|----------------|-----------------------------------------|
| all()          | 返回包含所有查询记录的列表                           |
| first()        | 返回查询的第一条记录，如果未找到，则返回 None               |
| get(id)        | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 None     |
| count()        | 返回查询结果的数量                               |
| first_or_404() | 返回查询的第一条记录，如果未找到，则返回 404 错误响应           |
| get_or_404(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 404 错误响应 |
| paginate()     | 返回一个 Pagination 对象，可以对记录进行分页处理          |

# 实现博客首页视图及样式
本套教程是一个Flask实战类教程，html/css/javascript等相关技术栈不会过多的去详细解释，那么就需要各位初学者尽可能的先去掌握这些基础知识，当然本套教程不需要你对其非常精通，但最起码得做到能看懂其意思！
## 静态文件
静态文件是相对动态的web应用而言的，一般是指css和js文件！ 网站应用部署的时候，这些静态文件通常由Nginx等静态文件服务器处理，但是在开发过程中， Flask 也能做好 这项工作。
一般，Flask的静态文件位于应用的 /static 中，模板文件位于应用的 /templates中。
因此上，我们需要在app/blog/目录下分别创建一个static及templates的文件夹，用来对应的存放博客的静态文件及模板文件！

## 创建博客首页视图
在app/blog/views/blog.py中通过蓝图的方式创建首页视图,代码如下：
Flask 会自动为你配置 Jinja2 模板引擎。
使用 render_template() 方法可以渲染模板，你只要提供模板名称和需要 作为参数传递给模板的变量就行了。
```text
from flask import Blueprint, render_template

bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


def index():
    """首页视图
    """
    return render_template('index.html')



```
在之前的蓝图应用章节我们对蓝图的使用做了大概的说明，其中这里新增了几个参数需要单独拉出来说一下，Blueprint类的template_folder参数就是指定该蓝图需要独立使用的模板文件夹，这个路径是相对路径或绝对路径，static_folder参数即设置静态文件目录，这样做的好处是我们就可以把每个功能模块拆分，静态文件和模板文件也可以独立拆分，这个思路是有借鉴django项目的布局方式，利于维护和后期的动态扩展！
index函数则就是一个python的普通函数，只是在返回的时候我们使用了Flask提供的render_template方法来动态渲染模板和载入上下文数据，启动posts=posts就是我们构造的一个上下文演示数据，下来将会在模板文件中使用该上下文，这里需要注意的是我们并没有使用装饰器的方法去绑定url，下来我们要介绍一个url和视图分离的url方式！

## add_url_rule方法分离视图与url
在项目目录（RealProject）的__init__.py中的工厂函数create_app底部创建如下代码
```text
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # 省略中间代码
    ...
    
    # 注册视图方法
    from app.blog import views as blog
    # 注册蓝图
    app.register_blueprint(blog.bp) 

    # 首页url
    app.add_url_rule(rule='/', endpoint='index', view_func=blog.index)
    return app

```
add_url_rule的参数解析：
* rule参数是真正的url，url开头必须以斜杠开始；
* endpoint参数是该url的端点，类似于django的name参数，它的作用是方便反查该url，一般的加载解析顺序是访问该url会先找该端点再找其关联的视图，然后开始处理逻辑，相当于url的id；
* view_func参数则是该url指向的函数，绑定url与函数！
之后只需要将register_bp函数引入工厂函数中即可,工厂函数代码修改如下：
```text
import os
from flask import Flask
from RealProject.settings import BASE_DIR
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    # instance_relative_config设置为True则代表开启从文件加载配置，默认为False
    app = Flask(__name__, instance_relative_config=True)

    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)
    # 绑定数据库
    db.init_app(app)
    # 注册migrate
    migrate.init_app(app, db)

    # 引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    # url引入
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    # 注册数据库模型
    from app.blog import models

    return app

```
## 创建博客首页模板文件
在app/blog/templates目录下创建index.html,这就是render_template方法第一个参数对应的模板文件，内容如下：
模板中用到的相关Jinja2模板语法，请自行查询文档理解
* Jinja2 模板文档 ： https://jinja.palletsprojects.com/en/3.1.x/templates/
```text
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock title %}</title>
    <link rel="stylesheet" href="{{ url_for('blog.static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('blog.static', filename='css/buefy.min.css') }}">
    {% block extra_head_style %}{% endblock extra_head_style %}   
</head>

<body>
    <div id="app" style="height:100%;">
        <div class="container is-fluid1" style="height:100%; ">
            <div class="is-block" style="height:100%;">
                <!-- 导航 -->
                {% block navbar %}     
                <template>
                    <b-navbar spaced shadow>
                        <template #brand>
                            <b-navbar-item>
                                <img src="{{ url_for('blog.static', filename='img/logo.png') }}" alt="FlaskBlog">
                            </b-navbar-item>
                        </template>
                        <template #start>
                            <b-navbar-item href="#">
                                Home
                            </b-navbar-item>
                            <b-navbar-item href="#">
                                Documentation
                            </b-navbar-item>
                            <b-navbar-dropdown label="Info">
                                <b-navbar-item href="#">
                                    About
                                </b-navbar-item>
                                <b-navbar-item href="#">
                                    Contact
                                </b-navbar-item>
                            </b-navbar-dropdown>
                        </template>

                        <template #end>
                            <b-navbar-item tag="div">
                                <div class="buttons">
                                    <a class="button is-primary">
                                        <strong>注册</strong>
                                    </a>
                                    <a class="button is-light">
                                       <strong>登录</strong>
                                    </a>
                                </div>
                            </b-navbar-item>
                        </template>
                    </b-navbar>
                </template>
                {% endblock navbar %}
                <!-- 导航 end -->

                {% block hero %}
                <section class="hero is-medium is-primary">
                    <div class="hero-body">
                        <p class="title">
                            Large hero
                        </p>
                        <p class="subtitle">
                            Large subtitle
                        </p>
                    </div>
                </section>
                {% endblock hero %}

                {% block main %} 
                <div class="box is-marginless is-shadowless is-radiusless">
                    <div class="columns is-multiline">
                        {% for post in posts %}
                        <div class="column is-4-fullhd">
                            <div class="card">
                                <div class="card-image">
                                    <figure class="image is-4by3">
                                        <img src="https://bulma.io/images/placeholders/1280x960.png"
                                            alt="Placeholder image">
                                    </figure>
                                </div>
                                <div class="card-content">
                                    <div class="media">
                                        <div class="media-content">
                                            <p class="title is-4"><a href="">Flask博客实战 - 掌握增删改查</a> </p>
                                        </div>
                                    </div>

                                    <div class="content">
                                        <p class=" has-text-grey is-size-7"> 
                                            既然我们选择了使用ORM框架，那就必须熟练掌握其提供的增删改查方法，在正式编写视图事前，
                                            本节内容我们先在shell环境中来了解和熟悉其增删改查的基础方法！
                                        </p>
                                        <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>

                    <nav class="pagination" role="navigation" aria-label="pagination">
                        <a class="pagination-previous is-disabled" title="This is the first page">Previous</a>
                        <a class="pagination-next">Next page</a>
                        <ul class="pagination-list">
                          <li>
                            <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">1</a>
                          </li>
                          <li>
                            <a class="pagination-link" aria-label="Goto page 2">2</a>
                          </li>
                          <li>
                            <a class="pagination-link" aria-label="Goto page 3">3</a>
                          </li>
                        </ul>
                    </nav>
                </div>
                {% endblock main %}



                {% block footer %}      
                <div class="footer has-background-black-ter is-marginless">
                    <div class="has-text-centered has-text-grey-light">
                        © 2022 <a class="has-text-grey-light" href="http://www.lotdoc.cn/blog/topic/detail/6/">FlaskBlog博客实战</a> 版权所有 备案号：陕ICP备20005686号
                    </div>
                </div>
                {% endblock footer %}
            </div>

        </div>
    </div>

    <script src="{{ url_for('blog.static', filename='js/vue.js') }}"></script>
    <script src="{{ url_for('blog.static', filename='js/buefy.min.js') }}"></script>
    {% block extra_foot_script %}{% endblock extra_foot_script %}
    <script>
        var app = new Vue({
            el: '#app',
            data: {},
            methods: {}
        })
    </script>
    {% block vue_script %}{% endblock vue_script %}
</body>

</html>
```
![img_9.png](img_9.png)

`index.html会被提示如图错误，不需要处理，忽略就好`

## 静态文件说明
```text
模板中我们看到加载静态文件的方法使用了{{ url_for('blog.static', filename='css/style.css') }}这样的语法，这是固定写法，第一个参数就是静态文件的路径，这里使用了蓝图来隔离了各应用之间的静态文件，那么blog.static即代表加载blog蓝图中的静态文件夹，filename则是静态文件的路径字符串，加载图片也是同样的方法！
```
本项目前端依赖的第三方框架有：
* buefy -- https://buefy.org/
* bulma -- https://bulma.io/
* vue2 -- https://cn.vuejs.org/

## 最终样式
![img_10.png](img_10.png)

![img_11.png](img_11.png)

# 创建用户相关应用
在前几个章节我们已经详细的说了创建视图及url的方式，也熟悉了基本的增删改查方法，那么我们就可以利用之前所学的知识来实现用户相关应用，并构造好基本的登录注册功能视图！
最开始我们创建目录的时候就在app文件夹下预留了一个auth的文件夹，相关登录注册以及用户相关的数据及视图模板都放到这个文件夹下边

## 创建用户相关应用
在app/auth/目录下参照blog目录创建相关文件，这次我们将models和views放到文件夹中，使其成为一个块
1、创建一个models的文件夹并在其内部创建一个__init__.py的文件及auth.py的文件
2、创建一个views的文件夹并在其内部创建一个__init__.py的文件及auth.py的文件
3、创建一个templates的文件夹并在其内部创建一个login.html的文件及register.html的文件

目录结构如下
```text
app/
    auth/
        __init__.py
        models/
            __init__.py
            auth.py
        views/
            __init__.py
            auth.py
        templates/
            login.html
            register.html
        static/
    blog/
    __init__.py
RealProject/

```
## 创建用户模型User
在models/auth.py文件中创建用户模型如下：
```text
from datetime import datetime
from RealProject import db


class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now, )  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间


class User(BaseModel):
    """用户模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(320), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    is_super_user = db.Column(db.Boolean, nullable=True, default=False)  # 超级管理员标识
    is_active = db.Column(db.Boolean, nullable=True, default=True)  # 是否为活跃用户
    is_staff = db.Column(db.Boolean, nullable=True, default=False)  # 是否允许登录后台

    def __repr__(self):
        return '<Category %r>' % self.username

```
在models/__init__.py中引入用户模型
```text
from .auth import User
```
在RealProject/__init__.py工厂函数中注册模型models
```text
import os
from flask import Flask
from RealProject.settings import BASE_DIR
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 实例化SQLAlchemy对象
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)

    # 递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 引入blog的视图文件
    from app.blog.views import blog
    app.register_blueprint(blog.bp)
    # 首页url
    app.add_url_rule(rule='/', endpoint='index', view_func=blog.index)

    # 绑定数据库
    db.init_app(app)
    # 注册migrate
    migrate.init_app(app, db)

    # 注册数据库模型
    from app.blog.models import blog
    from app.auth.models import auth

    return app

```
## 同步数据库
```text
$env:FLASK_APP = 'RealProject'
$env:FLASK_ENV = 'development'
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db init
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db migrate
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db upgrade
```

## 创建登录注册视图
在app/auth/views/auth.py文件中创建登录注册视图
```text
from flask import render_template, Blueprint, redirect, url_for, request

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录相关逻辑代码
        print("登录相关逻辑代码")

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 注册相关逻辑代码

        # 注册成功跳转到登录页
        return redirect(url_for('auth.login'))

    return render_template('register.html')
```
![img_12.png](img_12.png)

到这里我们的用户模型及登录注册视图的基本框架就已经做好了，下一章节我们将利用Flask-login这个第三方扩展来实现博客的登录功能，大家可以提前去看看该扩展的文档！

# 实现登录注册功能


上一章节我们已经创建了一个用户应用，并创建了用户模型，那么我们这节就开始实现一个简单的用户登录注册功能！
登录注册功能Flask有一个非常优秀地扩展Flask-login，我们可以选择使用这个扩展来实现，但为了学习我们暂时不使用这个第三方扩展，而是选择使用session来实现！

## 重新编写blog/templates/index.html
```text
{% extends 'base.html' %}
```
## 实现用户的登录功能(手写逻辑)
首先，我们需要完善登录的html页面, 路径为：app/auth/templates/login.html
在login.html中 extends的 base.html路径为：app/blog/templates/base.html(和index.html内容完全一致，但后续会更改)

```text
{% extends 'base.html' %}

{% block title %} 登录页 {% endblock title %}

{% block hero %}{% endblock hero %}

{% block main %}
<div class="box is-radiusless is-marginless" style="height: 80%;">
    <div class="columns is-centered">
        <div class="column is-5-fullhd">
            {% block auth_form %}
            <form action="" method="post" style="margin-top: 40%;" class="box">
                <div class=" has-text-centered mb-3">
                    <p class=" subtitle">登录</p>
                    <h1 class="title">FlaskBlog</h1>
                </div>

                <!-- 消息闪现 -->
                {% with messages = get_flashed_messages() %}
                <b-message type="is-danger">
                  {% if messages %}
                    <ul class=flashes>
                    {% for message in messages %}
                        <li>{{ message }}</li>
                    {% endfor %}
                    </ul>
                {% endif %}
                </b-message>
                {% endwith %}

                <div class="field">
                    <p class="control has-icons-left has-icons-right">
                      <input class="input" type="text" name="username" id="id_username" maxlength="128" placeholder="Username">
                      <span class="icon is-small is-left">
                        <i class="fas fa-envelope"></i>
                      </span>
                      <span class="icon is-small is-right">
                        <i class="fas fa-check"></i>
                      </span>
                    </p>
                  </div>
                  <div class="field">
                    <p class="control has-icons-left">
                      <input class="input" type="password" name="password" id="id_password" maxlength="320" minlength="6" placeholder="Password">
                      <span class="icon is-small is-left">
                        <i class="fas fa-lock"></i>
                      </span>
                    </p>
                  </div>
                  <div class="field">
                    <p class="control">
                      <input class="button is-success is-fullwidth" type="submit" value="Login">
                    </p>
                </div>
            </form>
            {% endblock auth_form %}
        </div>

    </div>

</div>
{% endblock main %}

```

代码详解：
这个登陆模板继承了base.html的样式，这个base.html中的模块及代码其实就是我们之前实现的首页，只是我们把他作为一个模板基类来继承他！
这段代码中其实就是写了一个输入账号密码的表单，其他多余的代码都是为了实现表单的样式而存在的！
```text
<input class="input" type="text" name="username" id="id_username" maxlength="128" placeholder="Username">
<input class="input" type="password" name="password" id="id_password" maxlength="320" minlength="6" placeholder="Password">

```
这里要特别说明的是这个input表单必须设置name属性，因为后端要根据此name属性来获取用户输入的值！其他属性则需要大家自行去了解学习！
登录功能的后端逻辑视图, 路径为：app/auth/views/auth.py
```text
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录视图
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth.User.query.filter_by(username=username).first()
        error = None
        if user is None:
            # 用户存在，验证密码是否正确，正确就登录
            error = '用户不存在，请先去注册'
        elif not check_password_hash(user.password, password):
            error = "密码不正确！"
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect('/')
        flash(error)

    return render_template('login.html')

```
代码详解： - request.method == 'POST'判断当前请求是否为post请求方式 - error = None 来初始化一个错误变量，如果未通过登录验证，把错误信息通过消息传送到页面提示用户
```text
user = auth.User.query.filter_by(username=username).first()
if user is None:
    error = '该用户不存在！'
elif not check_password_hash(user.password, password):
    error = '密码不正确.'
```

这段代码首先在数据库通过用户提交的用户名去查询该用户，用户不存在就会返回None返回错误提示，用户存在则判断密码是否正确，这里用到了一个check_password_hash()的方法，这是用来将密文密码解密后与用户输入密码比对方法，与之对应的有一个generate_password_hash()的方法用来加密明文密码保存到数据库！
```text
if error is None:
    session.clear()
    session['user_id'] = user.id
    return redirect(url_for('index'))
flash(error)
```
这段代码则是如果没有返回任何错误提示，说明该提交的表单符合我们的要求，并且数据库也存在该用户信息，那么我们只需要清空session，重新将session中的user_id设置为当前登录的id即可！
因此上在实现登录注册逻辑之前就必须引入这两个方法：
```text
from werkzeug.security import check_password_hash, generate_password_hash
```
登录功能虽然实现了，但我们数据库目前还没有任何一个用户，所以此时就应该要去实现用户的注册功能，向数据库新增用户，大概的逻辑是，用户输入用户名及两次密码，先判断该用户是否已经存在，存在则提示更换用户名，不存在则向数据库创建该用户信息，并清空session，重新设置user_id的值为注册用户的id，以达到注册成功后自动登录的目的！

## 实现用户的注册功能
首先，我们需要完善注册的html页面, 路径为：app/auth/templates/register.html
```text
{% extends 'login.html' %}

{% block title %}注册{% endblock title %}

{% block auth_form %}
<form action="" method="post" style="margin-top: 40%;" class="box">
    <div class=" has-text-centered mb-3">
        <p class=" subtitle">注册</p>
        <h1 class="title">FlaskBlog</h1>
    </div>
     <!-- 消息闪现 -->
     {% with messages = get_flashed_messages() %}
     <b-message type="is-danger">
       {% if messages %}
         <ul class=flashes>
         {% for message in messages %}
             <li>{{ message }}</li>
         {% endfor %}
         </ul>
     {% endif %}
     </b-message>
     {% endwith %}

    <div class="field">
        <p class="control has-icons-left has-icons-right">
            <input class="input" type="text" name="username" id="id_username" maxlength="128" placeholder="Username">
            <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
                <i class="fas fa-check"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control has-icons-left">
            <input class="input" type="password" name="password" id="id_password" maxlength="320" minlength="6" placeholder="Password">
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control has-icons-left">
            <input class="input" type="password" name="password1" id="id_password1" maxlength="320" minlength="6" placeholder="Password1">
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control">
            <input class="button is-success is-fullwidth" type="submit" value="Register">
        </p>
    </div>
</form>
{% endblock auth_form %}
```

这是注册页面的html，大家自行理解下，这里着重说一个我们在视图中通过flash()传递出来的消息，在模板中由以下代码接收！
```text
<!-- 消息闪现 -->
{% with messages = get_flashed_messages() %}
    <b-message type="is-danger">
    {% if messages %}
        <ul class=flashes>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}
    </b-message>
{% endwith %}
```
注册功能的后端逻辑视图, 路径为：app/auth/views/auth.py
```text
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 注册相关逻辑代码
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        user = auth.User.query.filter_by(username=username).first()

        if password != password1:
            flash("两次密码输入不一致！")
            return redirect('/auth/register')

        if user:
            flash('改用已经存在，请勿重复注册')
            return redirect('/auth/register')
        else:
            # 添加一个用户信息到数据库
            u = User(username=username, password=generate_password_hash(password1))
            db.session.add(u)
            db.session.commit()

            # 自动登录的效果
            session.clear()
            session['user_id'] = u.id
        return redirect('/')

    return render_template('register.html')

```


这个注册的逻辑基本上涵盖了我们之前所有章节学到的知识点，这里就不再过多的去一一解释代码，大家可自行理解并完善注释！
## 实现用户退出登录功能
通过登录和注册功能的实现，我们已经清楚的知道，用户是否登录其实是判断session会话中是否存在用户的id来决定，那么推出登录，我们只需要清除session会话中的用户id即可，这里我们直接选择清空session的方式实现推出功能！
```text
@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect('/')
```
## 在模板中获取用户信息
```text
@bp.before_app_request
def load_logged_in_user():
    # 每个请求之前都回去session中查看user_id来获取用户
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = auth.User.query.get(int(user_id))
```
bp.before_app_request()注册一个在视图函数之前运行的函数，无论请求什么 URL。 都会先检查用户 ID 是否存储在会话中，并从数据库获取该用户的数据，将其存储在 g.user 上，该数据在请求期间持续。
注册完这个函数之后，我们就可以在index.html中的导航的最右侧通过g.user的返回值，判断用户是否已经登录，显示不同的信息！

app/blog/templates/base.html
```text
<!-- 导航 -->
{% block navbar %}     
<template>
    <b-navbar spaced shadow>
        <template #brand>
            <b-navbar-item>
                <img src="{{ url_for('blog.static', filename='img/logo.png') }}" alt="FlaskBlog">
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item href="#">
                Home
            </b-navbar-item>

        ... 省略部分代码
        </template>


        <template #end>
            <b-navbar-item tag="div">
                <!-- 判断用户是否已登录 -->
                {% if g.user %}              
                <div class=" buttons">
                    <!-- 获取用户信息 -->
                    <a class="button is-primary">欢迎您 {{ g.user['username'] }}</a>
                    <a class="button is-success">个人中心</a>
                    <!-- 显示推出按钮 -->
                    <a class="button is-danger" href="{{ url_for('auth.logout') }}">退出</a>
                </div>
                {% else %}
                <!-- 用户未登录，显示登录注册按钮 -->
                <div class="buttons">
                    <a class="button is-primary" href="{{ url_for('auth.register') }}">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light" href="{{ url_for('auth.login') }}">Log in</a>
                </div>
                {% endif %}
            </b-navbar-item>
        </template>
    </b-navbar>
</template>
{% endblock navbar %}
<!-- 导航 end -->
```

## 实现login_required装饰器
对于像下一章节我们要实现的用户中心以及管理后台，则必须是带有权限的访问，最基本的权限应该是必须是登录用户，那么所以说对于那些未登录的用户我们需要拒绝访问的功能！
这个其实思路也非常简单，既然在实现模板中调用用户信息的时候，我们把当前登录的用户信息添加到了g对象，那么我们只需要判断g.user的返回值是否为None即可判断用户是否登陆！
```text
def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
```
到这里关于用户登录注册相关的基本权限问题我们就完成了，注意这些视图函数都在app/auth/views/auth.py文件中！
## 完整的auth.py
```text
import functools

from flask import render_template, Blueprint, redirect, url_for, request, session, flash, g
from app.auth.models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db

from app.auth.models.auth import User

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


@bp.before_app_request
def load_logged_in_user():
    # 每个请求之前都回去session中查看user_id来获取用户
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = auth.User.query.get(int(user_id))


def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录视图
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth.User.query.filter_by(username=username).first()
        error = None
        if user is None:
            # 用户存在，验证密码是否正确，正确就登录
            error = '用户不存在，请先去注册'
        elif not check_password_hash(user.password, password):
            error = "密码不正确！"
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect('/')
        flash(error)

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 注册相关逻辑代码
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        user = auth.User.query.filter_by(username=username).first()

        if password != password1:
            flash("两次密码输入不一致！")
            return redirect('/auth/register')

        if user:
            flash('改用已经存在，请勿重复注册')
            return redirect('/auth/register')
        else:
            # 添加一个用户信息到数据库
            u = User(username=username, password=generate_password_hash(password1))
            db.session.add(u)
            db.session.commit()

            # 自动登录的效果
            session.clear()
            session['user_id'] = u.id
        return redirect('/')

    return render_template('register.html')


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect('/')

```
# 使用 WTForms 进行表单验证
上一章节我们通过在html中直接编写表单的方式进行数据传递，并且在视图中对前端传递的数据进行了简单的认证，但是如果把验证数据的代码与逻辑混合在一起，将使得视图的代码不够清晰，并且难以维护，稍加疏忽就会产生验证漏洞，如果细心的同学其实可以发现，在之前的登录注册中我们一直没有对空表单进行验证，当然这是我故意为之，但如果在生产环境，这将是一个灾难的开始，所以，在编程中无论是前端还是后端都要求要对数据进行验证，作为后端，更要保持一种永远不相信前端传递数据的态度去做数据校验。
本章节我们将使用Flask官方推荐的Flask-WTF扩展来重构我们的登录注册表单！

## 关于Flask-WTF
Flask-WTF是Flask 和 WTForms 的简单集成，包括 CSRF、文件上传和 reCAPTCHA。
* 安装Flask-WTF：
```text 
E:\pythonproject\FlaskBlog\venv\Scripts\pip.exe install Flask-WTF
```
## 创建登录注册表单类
在app/auth/目录下新建一个forms.py的文件,所有的表单验证代码都放到这个文件当中！
## 构建表达验证
```text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash
from .models.auth import User


class LoginForm(FlaskForm):
    # 登陆表单

    def qs_username(username):
        # 对该字段进行在传递之前处理
        u = f'{username}'
        print(u)
        return username

    username = StringField('username', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
        ], filters=(qs_username,))
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
        ])

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            error = '该用户不存在！'
            raise ValidationError(error)
        elif not check_password_hash(user.password, form.password.data):
            raise ValidationError('密码不正确!')

```
代码详解：
* class LoginForm(FlaskForm): 创建了一个登录表单类，继承了FlaskForm类
* StringField, PasswordField
* 这些都是wtforms内置的字段，负责呈现和数据转换。
* 官方文档：https://wtforms.readthedocs.io/en/3.0.x/fields/
* 他继承自Filed的基类，其中有一些比较重要的参数我们大概在这里理解一下！
* 第一个字符串其实是该类的label参数，字段的标签，也就是转换到html中的label!
* validators传入对该字段的一些验证器，在提交数据之前对数据进行验证！
* filters这个参数比较特殊，官方文档并没有对其详细说明，只说是筛选器，其实怎么说就是在额外的方法中对该字段的值提前处理过滤，元组中的每个值都是一个回调函数，函数不需要传入括号，但这个回调函数默认有一个参数，这个参数就是本身该字段的值，所以在定义该函数时就必须传入一个参数！例如：我们定义username之前定义的这个方法！
```text
def qs_username(username):
    # 对该字段进行在传递之前处理
    u = f'{username}'
    print(u)
    return username
```
备注：必须返回处理后的这个参数，否则会触发DataRequired验证器，后端获取不到该表单的值！
*  DataRequired, Length 这是内置的验证器，第一个是验证字段是否为空，第二个Length是验证输入长度，当然内置的还有很多，这里就不一一列举，具体我们可参考文档！
官方文档： https://wtforms.readthedocs.io/en/3.0.x/validators/#custom-validators

## 自定义验证用户名和密码
在之前的视图函数中我们对用户名和密码都做了校验，现在我们需要把验证的代码全部移动到表单类中，代码如下：
```text
def validate_username(form, field):
    user = User.query.filter_by(username=field.data).first()
    if user is None:
        error = '该用户不存在！'
        raise ValidationError(error)
    elif not check_password_hash(user.password, form.password.data):
        raise ValidationError('密码不正确')
```
* validate_username(form, field)
这个函数的写法是固定的validate_{filed},validate_后边的filed是指你需要验证的某个字段名，比如我们这个验证，他主要就是对username字段进行验证，这个函数中参数的filed就是这个字段，通过field.data就可以获取到usernam的值。form参数则指代的是整个表单，可以用form.{filed}.data的方式获取表单类中某个具体字段的值！

## 构建注册表单
当了解了登录表单后，我们完全就可以参照登录表单去实现注册表单，代码如下：
路径：app/auth/forms.py
```text
class RegisterForm(FlaskForm):
    # 注册表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"),
        Length(min=2, max=32, message="超过限制字数！")
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(min=2, max=32, message="超过限制字数！"),
        EqualTo('password1', message='两次密码输入不一致！')
        ])
    password1 = PasswordField('password1')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            error = '该用户名称已存在！'
            raise ValidationError(error)
```
这里唯一需要注意的是两次密码是否输入一致，我们用了一个内置的验证器EqualTo,使用方式可完全参照代码，他会自动校验password和password1输入的值是否一致！

## 重构登录和注册视图
* 路径：app/auth/views/auth.py
```text
from ..forms import LoginForm, RegisterForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录视图
    redirect_to = request.args.get('redirect_to')
    form = LoginForm()
    if form.validate_on_submit():
        user = auth.User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['user_id'] = user.id
        if redirect_to is not None:
            return redirect(redirect_to)
        return redirect('/')
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册视图
    form = RegisterForm()
    if form.validate_on_submit():
        user = auth.User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        session.clear()
        session['user_id'] = user.id
        return redirect('/')
    return render_template('register.html', form=form)
```
1、首先从forms.py中引入了我们定义的登录（LoginForm）和注册（RegisterForm）表单类！
2、form = RegisterForm() 实例化表单类
3、if form.validate_on_submit(): 验证前端传递的数据是否有效，并且会自动判断是POST请求还是GET请求！
4、 数据验证通过则进入之后的逻辑，未验证通过则返回我们在表单类中传入的验证提示！

## 模板中调用验证信息

我们以调用username字段的验证提示为例，在模板中加入这段代码即可获得错误提示!（修改login.html文件）
```text
<!-- 表单验证 -->
{% if form.username.errors %}
<b-message type="is-danger">
    <ul class="errors">
        {% for error in form.username.errors %}
            <li>{{ error }}</li>
        {% endfor %}
    </ul>
</b-message>
{% endif %}

省略代码。。。
<!-- 消息闪现 -->
```
## 重构登录注册html模板
路径：app/auth/templates/login.html 以登陆表单为例，代码如下：
```text
{% extends 'base.html' %}

{% block title %} 登录页 {% endblock title %}

{% block hero %}{% endblock hero %}

{% block main %}
<div class="box is-radiusless is-marginless" style="height: 80%;">
    <div class="columns is-centered">
        <div class="column is-5-fullhd">
            {% block auth_form %}
            <form action="" method="post" style="margin-top: 40%;" class="box">
                <div class=" has-text-centered mb-3">
                  <p class=" subtitle">登录</p>
                  <h1 class="title">FlaskBlog</h1>
                </div>
                {{ form.csrf_token }}
                <!-- 消息闪现 -->
                {% with messages = get_flashed_messages() %}
                <b-message type="is-danger">
                  {% if messages %}
                  <ul class=flashes>
                    {% for message in messages %}
                    <li>{{ message }}</li>
                    {% endfor %}
                  </ul>
                  {% endif %}
                </b-message>
                {% endwith %}

                <!-- 表单验证 -->
                {% if form.username.errors %}
                <b-message type="is-danger">
                  <ul class="errors">
                    {% for error in form.username.errors %}
                    <li>{{ error }}</li>
                    {% endfor %}
                  </ul>
                </b-message>
                {% endif %}

                <div class="field">
                  <p class="control has-icons-left has-icons-right">
                    {{ form.username(class='input', placeholder='Username') }}
                    <span class="icon is-small is-left">
                      <i class="fas fa-envelope"></i>
                    </span>
                    <span class="icon is-small is-right">
                      <i class="fas fa-check"></i>
                    </span>
                  </p>
                </div>
                <div class="field">
                  <p class="control has-icons-left">
                    {{ form.password(class='input', placeholder='Password') }}
                    <span class="icon is-small is-left">
                      <i class="fas fa-lock"></i>
                    </span>
                  </p>
                </div>
                <div class="field">
                  <p class="control">
                    <input class="button is-success is-fullwidth" type="submit" value="Login">
                  </p>
                </div>
              </form>
            {% endblock auth_form %}
        </div>

    </div>

</div>
{% endblock main %}
```
{{ form.csrf_token }} 隐式的创建一个csrftoken的表单
{{ form.username(class='input', placeholder='Username') }} 这样就可以直接获得一个表单html并自动渲染，向该表单增加书香的方式就是像代码中这样传入参数和值即可，当然也可以提前在表单类中定义！
剩下的注册表单，就当是给大家留作的一个作业，大家自行去参照登录表单完善重构一下，加油哦！我相信你可以！
到这里我们的表单验证就大概了解了，之后的章节就是基本的增删改查以及表单验证，都是基于我们这些章节学习的知识点，所以之后的章节就不会过多的去讲解每行代码的意思，重心放在逻辑的展示上，如果基础较差的同学，到这里，可以去反复的把前边所有章节的内容去练习，写代码其实就是写的多了就会了，也就理解了，练习 练习 再练习

路径：app/auth/templates/register.html 以登陆表单为例，代码如下：
```text
{% extends 'login.html' %}

{% block title %}注册{% endblock title %}

{% block auth_form %}
<form action="" method="post" style="margin-top: 40%;" class="box">
    <div class=" has-text-centered mb-3">
        <p class=" subtitle">注册</p>
        <h1 class="title">FlaskBlog</h1>
    </div>
    {{ form.csrf_token }}
    <!-- 表单验证 -->
    {% if form.username.errors %}
    <b-message type="is-danger">
      <ul class="errors">
        {% for error in form.username.errors %}
        <li>{{ error }}</li>
        {% endfor %}
      </ul>
    </b-message>
    {% endif %}

     <!-- 消息闪现 -->
     {% with messages = get_flashed_messages() %}
     <b-message type="is-danger">
       {% if messages %}
         <ul class=flashes>
         {% for message in messages %}
             <li>{{ message }}</li>
         {% endfor %}
         </ul>
     {% endif %}
     </b-message>
     {% endwith %}

    <div class="field">
        <p class="control has-icons-left has-icons-right">
            {{ form.username(class='input', placeholder='Username') }}
            <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
                <i class="fas fa-check"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control has-icons-left">
            {{ form.password(class='input', placeholder='Password') }}
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control has-icons-left">
            {{ form.password1(class='input', placeholder='Password1') }}
            <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
            </span>
        </p>
    </div>
    <div class="field">
        <p class="control">
            <input class="button is-success is-fullwidth" type="submit" value="Register">
        </p>
    </div>
</form>
{% endblock auth_form %}
```
## 将auth注册到工厂函数中
```text
    # 注册视图方法
    from app.blog.views import blog as blog
    from app.auth.views import auth as auth
    # 注册蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
```
# 到这里结束

# 创建后台管理应用
Flask与django最大的不同就在这里，django的理念是快速开发，所以他尽可能多的帮我们集成了所有web的功能，包括了一个强大的admin后台管理系统！
而Flask倡导的是自由度，因此无论大小的系统，只要牵扯到数据管理的增删改查的地方都要我们手动去实现，当然Flask也有对应的第三方扩展，但本教程更多的是让大家熟悉Flask，而不是学习扩展，所以我们不回去用第三方扩展来实现这里的功能！
## 创建后台管理应用admin
在app/目录下创建一个admin/模块目录，与blog和auth模块的目录结构一致，也就是我们所说的应用！目录结构如下：
```text
app/
    admin/
        __init__.py
        forms.py
        models/
        views/
        templates/
        static/
```
# 创建各功能视图
## 创建admin主页视图
在app/admin/views.py中创建如下代码
```text
from ctypes import pointer
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from app.auth.views.auth import login_required

# from app.blog.models import Category, Post, Tag
# from app.auth.models import User
# from .models import Banner
# from .forms import CategoryForm, PostForm, TagForm, CreateUserForm


bp = Blueprint('admin', __name__, url_prefix='/admin',
               template_folder='templates', static_folder='static')


@bp.route('/')
@login_required
def index():
    # 主页视图
    return render_template('admin/index.html')

```
在app/admin/templates/admin目录下创建index.html
```text
{% extends 'base.html' %}

{% block title %}
{{ g.user['username'] }}-个人中心
{% endblock title %}

{% block hero %}{% endblock hero %}

{% block box %}
<div class="columns">
    <div class="column is-2">
        <div class="card is-shadowless" style="border-right:solid 1px #eee">
            <div class="card-content">
                <aside class="menu">
                    <p class="menu-label">
                        仪表板
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if request.path == '/admin/' %}is-active{% endif %}"
                            href="{{ url_for('admin.index') }}">主页</a></li>
                        <!-- <li><a>Customers</a></li> -->
                    </ul>
                    <p class="menu-label">
                        博客分类
                    </p>
                    <ul class="menu-list">
                        <li><a href="">分类管理</a></li>
                    </ul>
                    <p class="menu-label">
                        文章管理
                    </p>
                    <ul class="menu-list">
                        <li><a href="">文章管理</a></li>
                    </ul>
                    <p class="menu-label">
                        用户管理
                    </p>
                    <ul class="menu-list">
                        <li><a>用户管理</a></li>
                        <li><a>修改密码</a></li>
                    </ul>
                </aside>
            </div>
        </div>
    </div>
    <div class="column">
        {% block member %}
        <div class="tile is-ancestor">
            <div class="tile is-parent">
                <article class="tile is-child notification is-info is-light">
                    <div class="content">
                        <p class="title">100</p>
                        <p class="subtitle">文章数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-success is-light">
                    <div class="content">
                        <p class="title">50</p>
                        <p class="subtitle">用户数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-warning is-light">
                    <div class="content">
                        <p class="title">150</p>
                        <p class="subtitle">评论数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
        </div>
        {% endblock member %}
    </div>
</div>
{% endblock box %}
```
## 重构auth/views/auth.py中的login_required视图
```text
def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect_to = f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
        return view(**kwargs)

    return wrapped_view
```

最后，别忘了在项目目录RealProject/init.py中注册该管理后台的蓝图
```text
def register_bp(app: Flask):
    # 注册视图方法
    from app.blog import views as blog
    from app.auth import views as auth
    from app.admin import views as admin
    # 注册蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    # 首页url
    app.add_url_rule(rule='/', endpoint='index', view_func=blog.index)
```
至此，我们的管理后台主页以及大的框架就搭建完成，下一章节我们将通过分类管理的增删改查来学习如何深度的利用Flask-WTF及Flask-sqlalchemy两个扩展实现我们的基本业务需求！

# 最终效果展示
管理后台我们将大概分类为如下几个：
* 主页
![img_13.png](img_13.png)
* 分类管理
![img_14.png](img_14.png)

![img_15.png](img_15.png)

* 文章管理
* 草稿箱
* 用户管理
那么，最终的几个页面基本上都与这几个布局和样式一致，尽可能的以最简单的代码和最明了的逻辑处理我们的业务，这一部分我们目前不考虑权限的问题，到最后我们再统一处理权限！

# 实现博客的分类管理
一般的后台管理都包含了该模块的增删改查的基本操作，我们也是以这样的思路先去简单的实现博客分类的增删改查操作！
* 最终效果如下：

![img_16.png](img_16.png)

![img_17.png](img_17.png)

## 实现查看分类列表
基本的逻辑思路是：查询出所有分类列表数据，并对其分页！
在app/admin/views.py中创建分类列表视图，代码如下：
```text
@bp.route('/category')
@login_required
def category():
    # 查看分类
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(-Category.add_date).paginate(page=page, per_page=10, error_out=False)
    category_list = pagination.items
    return render_template('admin/category.html', category_list=category_list, pagination=pagination)
```
这里的这个login_required装饰器就是我们对该视图进行了验证，只有登录的用户才可以访问！
```text
page = request.args.get('page', 1, type=int)
```
这行代码是说从一个GET请求中获取一个page的参数，默认值是1，类型必须为int，那么最终反映到url当中就是这样的：http://127.0.0.1:5000/admin/category?page=1这个page的值就是
```text
pagination = Category.query.order_by(-Category.add_date).paginate(page, per_page=10, error_out=False)
```
这行代码查询出所有的分类数据，通过order_by()方法按照发布时间进行倒序排列，在使用paginate()方法进行分页，per_page=10代表每页显示数量，超过该设置的数量则进行分页，error_out=False代表是否访问不存在的分页时显示错误页面，False是不显示！
category_list = pagination.items 获取分页后的数据！
这里最后我们将pagination和category_list传入到上下文中，这样就可以在模板中使用这两个数据进行查新显示！

## 创建列表页html模板
在app/admin/templates/admin/目录下创建category.html模板
```text
{% extends 'admin/index.html' %}    

{% block member %}
<div class="is-block">
    <div class=" is-pulled-left">
        <h1 class=" is-size-4">
            <span class="icon">
                <i class="mdi mdi-receipt-outline"></i>
            </span>
            分类管理
        </h1>
    </div>

    {% block button %}
    <div class=" is-pulled-right">
        <a href="" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加分类</span>
        </a>
    </div>
    {% endblock button %}
    <div class="is-clearfix"></div>
    <div class=" dropdown-divider"></div>

    <!-- 消息闪现 -->
    {% with messages = get_flashed_messages() %}
    <b-message type="is-success">
      {% if messages %}
      <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </b-message>
    {% endwith %}
</div>

{% block table_content %}
<div class="table-container">
    <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
            <tr>
              <th>ID</th>
              <th>分类名称</th>
              <th>分类图标</th>
              <th>发布日期</th>
              <th>操作</th>
            </tr>
        </thead>
        <tbody>

            {% for cate in category_list %}       
            <tr>
                <td>{{ cate.id }}</td>
                <td>{{ cate.name }}</td>
                <td>{{ cate.icon }}</td>
                <td>{{ cate.add_date }}</td>
                <td>
                    <div class="tags">
                        <a href="" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<nav class="pagination is-small" role="navigation" aria-label="pagination">
    {% if pagination.has_prev %}
    <a href="{{ url_for('admin.category') }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
    {% endif %}
    {% if pagination.has_next %}
    <a href="{{ url_for('admin.category') }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
    {% endif %}

    <ul class="pagination-list">        
        {% for page in pagination.iter_pages() %}
            {% if page %} 
                {% if page != pagination.page %}
                <li>
                    <a href="{{ url_for('admin.category') }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% else %}
                <li>
                    <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% endif %}
            {% else %}
                <span class=pagination-ellipsis>&hellip;</span>
            {% endif %}
        {% endfor %}

    </ul>
</nav>

{% endblock table_content %}
{% endblock member %}
```
## 实现添加博客分类
提到添加和修改，自然是离不开表单，那么第一步就是先创建表单类！
在app/admin/forms.py中创建Category的表单类
```text
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryCreateForm(FlaskForm):
    # 分类表单
    name = StringField('分类名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    icon = StringField('分类图标', validators=[ 
        Length(max=256, message="不符合字数要求！")
    ])
```

在app/admin/views.py中创建新增分类视图

```text
@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    # 增加分类
    form = CategoryCreateForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)
```
这个增加分类的逻辑和注册用户的逻辑基本一致，这里就不再过多的赘述每行代码的意思！
## 创建表单模板
在app/admin/templates/admin/目录下创建一个category_form.html
```text
{% extends 'admin/category.html' %}

{% block button %}{% endblock button %}


{% block table_content %}
    <form action="" method="post" class="mt-4">
        {{ form.csrf_token }}
        <div class="field">
            {{ form.name.label(class='label') }}
            <div class="control">
                {{ form.name(class='input', placeholder='分类名称') }}
            </div>
        </div>
        <div class="field">
            {{ form.icon.label(class='label') }}
            <div class="control">
                {{ form.icon(class='input', placeholder='分类图标') }}
            </div>
        </div>
        <div class="is-block">
            <div class="box has-background-light is-shadowless level">
                <a href="" class=" is-danger button level-left">删除</a>
                <div class="level-right">
                    <a href="{{ url_for('admin.category') }}" class="button is-primary is-light mr-2">返回</a>
                    <input type="submit" value="保存" class=" button is-success">
                </div>
            </div>
        </div>

    </form>
{% endblock table_content %}
```
最后修改添加分类按钮的url即可：

路径：app/admin/templates/admin/category.html
```text
{% block button %}
    <div class=" is-pulled-right">
        <a href="{{ url_for('admin.category_add') }}" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加分类</span>
        </a>
    </div>
{% endblock button %}
```
## 实现修改博客分类
修改的思路基本和保存的思路一致，唯一不同的是修改时需要在表单内回显数据，并且修改的是当前数据对象！

路径：app/admin/views.py
```text
@bp.route('/category/edit/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def category_edit(cate_id):
    # 增加分类
    category = Category.query.get(cate_id)
    form = CategoryCreateForm(name=category.name, icon=category.icon)
    if form.validate_on_submit():
        category.name = form.name.data
        category.icon = form.icon.data
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)
```

这里的代码也非常简单，首先是在url中和函数中传入了需要修改的当前分类id主键，再通过主键通过get的方式直接查询到该条信息！

回显数据到表单，这里单独说一下，只需要将个字段的值赋值给表单类即可：
```text
form = CategoryCreateForm(name=category.name, icon=category.icon)
```
这样我们的增加数据和修改数据就可以通用一个表单模板和表单类！

之后的修改操作我们在增删改查以及注册用户的时候做了详细的解说，这里大家就自行理解下！

最后，只需要在每条数据的编辑按钮引入该url即可
路径：app/admin/templates/admin/category.html
```text
<a href="{{ url_for('admin.category_edit', cate_id=cate.id) }}" class="tag is-success is-light">
    <span class="icon">
        <i class="mdi mdi-square-edit-outline"></i>
    </span>
    编辑
</a>
```
## 实现删除博客分类
这里的删除方案有两种，一种是直接通过get请求删除，只要点击这个删除链接数据就从数据库清除掉；另外一种方案是通过post请求删除，这种就可以在创建一个删除确认页通过get请求展示，问是否要真的删除，然后改页的确认按钮才是真正的发送post请求去删除数据@！

那么，为了演示，我们这里采用第一种get的方式！

在app/admin/views.py中创建删除视图

```text
@bp.route('/category/delete/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def category_del(cate_id):
    # 增加分类
    category = Category.query.get(cate_id)
    if category:  
        db.session.delete(category)
        db.session.commit()
        flash(f'{category.name}分类删除成功')
        return redirect(url_for('admin.category'))
```
这个删除和编辑的逻辑基本一致，在url中传入当前分类的id主键，通过主键获取到该条数据，如果该条数据存在，则执行删除操作，这样做的好处就是不需要再去访问一次确认页，访问该url就可以直接删除，弊端就是没有后悔的余地，误删的后果就得自己承担了！

最后，在删除按钮上增加该url即可
```text
<a href="{{ url_for('admin.category_del', cate_id=cate.id) }}" class="tag is-danger is-light">
    <span class="icon">
        <i class="mdi mdi-trash-can-outline"></i>
    </span>
    删除
</a>
```
最后在admin主页增加分类管理的url
路径：admin/templates/admin/index.html

```text
                    <ul class="menu-list">
                        <li><a class="{% if 'category' in request.path %}is-active{% endif %}" 
                               href="{{ url_for('admin.category') }}">分类管理</a></li>
                    </ul>
```

到这里，我们对博客分类的增删改查就基本做完了，掌握的比较好的同学就可以模仿着去实现一下文章管理的增删改查咯！

## 实现文章管理
文章管理的增删改查与我们在上一章节的分类增删改查基本一致，唯一不同的是添加文章的时候会同时添加分类及标签，一个是一对多的关系一个是多对多的关系，所以这一章节我们主要掌握这一个知识点即可！
最终效果如下：
![img_3.png](img_3.png)

![img_4.png](img_4.png)

## 实现查看文章列表
基本的逻辑思路是：查询出所有文章列表数据，并对其分页！

在app/admin/views.py中创建分类列表视图，代码如下：
```text
@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('admin/article.html', post_list=post_list, pagination=pagination)
```
## 创建列表页html模板
在app/admin/templates/admin/目录下创建article.html模板
```text
{% extends 'admin/index.html' %}    

{% block member %}
<div class="is-block">
    <div class=" is-pulled-left">
        <h1 class=" is-size-4">
            <span class="icon">
                <i class="mdi mdi-file-document-multiple-outline"></i>
            </span>
            文章管理
        </h1>
    </div>
    {% block button %}
    <div class="is-pulled-right">
        <a href="" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加文章</span> 
        </a>
    </div>
    {% endblock button %}
    <div class="is-clearfix"></div>
    <div class=" dropdown-divider"></div>

    <!-- 消息闪现 -->
    {% with messages = get_flashed_messages() %}
    <b-message type="is-success">
      {% if messages %}
      <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </b-message>
    {% endwith %}
</div>
{% block table_content %}
<div class="table-container">
    <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
            <tr>
              <th>ID</th>
              <th>标题</th>
              <th>发布状态</th>
              <th>归属分类</th>
              <th>标签</th>
              <th>发布日期</th>
              <th>操作</th>
            </tr>
        </thead>
        <tbody>

            {% for post in post_list %}   
            <tr>
                <td>{{ post.id }}</td>
                <td>{{ post.title }}</td>
                <td>{{ post.has_type.name }}</td>
                <td>{{ post.category.name }}</td>
                <td>{{ post.tags|join(',') }} </td>
                <td>{{ post.add_date }}</td>
                <td>
                    <div class="tags">
                        <a href="" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
                    </div>
                </td>
            </tr>
            {% endfor %}

        </tbody>
    </table>
</div>

<nav class="pagination is-small" role="navigation" aria-label="pagination">
    {% if pagination.has_prev %}
    <a href="{{ url_for('admin.article') }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">上一页</a>
    {% endif %}
    {% if pagination.has_next %}
    <a href="{{ url_for('admin.article') }}?page={{ pagination.next_num }}" class="pagination-next">下一页</a>
    {% endif %}

    <ul class="pagination-list">        
        {% for page in pagination.iter_pages() %}
            {% if page %} 
                {% if page != pagination.page %}
                <li>
                    <a href="{{ url_for('admin.article') }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% else %}
                <li>
                    <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% endif %}
            {% else %}
                <span class=pagination-ellipsis>&hellip;</span>
            {% endif %}
        {% endfor %}

    </ul>
</nav>
{% endblock table_content %}
{% endblock member %}
```
## 实现添加博客内容
在app/admin/forms.py中创建Post的表单类
```text
class PostForm(FlaskForm):
    # 添加文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])
    has_type = RadioField('发布状态', 
        choices=(PostPublishType.draft.name, PostPublishType.show.name), 
        default=PostPublishType.show.name)
    category_id = SelectField(
        '分类', 
        choices=None, 
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ]
    )
    content = TextAreaField('文章详情', 
        validators=[DataRequired(message="不能为空")]
    )
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)    
```

这个表单类里边我们多了几个新的表单类，我们来逐一认识下

RadioField也就是单选按钮表单，其中chioces参数则是定义他的选项,我们这里直接引入定义的PostPublishType的名称即可

SelectField是下拉表单类，choices是选项，coerce定义该表单值得类型，默认为str，我们这里传递的是分类的主键，所以改为int

SelectMultipleField多选表单，其他参数均与SelectField一致

TextAreaField则是多行输入表单

在app/admin/views.py中创建新增文章视图
```text
@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 增加文章
    form = PostForm()
    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            desc=form.desc.data, 
            has_type=form.has_type.data, 
            category_id=int(form.category_id.data),
            content=form.content.data,
        )
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章添加成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)
```
这里唯一要注意的是我们在表单创建的时候默认设置的分类和标签的选项值是None，那么在视图中初始化表单后，必须设置choices属性的值

```text
form = PostForm()
form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]
```
这样子我们表单中就直接从数据库获取到了该两项的值！

其次再给category_id赋值的时候应该指定其类型为int

多对多赋值,记住列表的每一个值必须为一个对象：post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]

## 创建表单模板
在app/admin/templates/admin/目录下创建一个article_form.html
```text
{% extends 'admin/article.html' %}

{% block button %}{% endblock button %}


{% block table_content %}
    <form action="" method="post" class="mt-4">
        {{ form.csrf_token }}
        <div class="field">
            {{ form.title.label(class='label') }}
            <div class="control">
                {{ form.title(class='input', placeholder='标题') }}
            </div>
        </div>
        <div class="field">
            {{ form.desc.label(class='label') }}
            <div class="control">
                {{ form.desc(class='input', placeholder='描述') }}
            </div>
        </div>

        <div class="field">
            {{ form.category_id.label(class='label') }}
            <div class="control">
                <div class="select is-fullwidth">
                    {{ form.category_id }}
                </div>
            </div>
        </div>

        <div class="field">
            {{ form.content.label(class='label') }}
            <div class="control">
                {{ form.content(class='textarea', rows="10", placeholder='文章详情') }}
            </div>
        </div>

        <div class="field">
            {{ form.tags.label(class='label') }}
            <div class="control">
                <div class="select is-fullwidth is-multiple">
                    {{ form.tags(size='5') }}
                </div>
            </div>
        </div>

        <div class="field is-horizontal">
            {{ form.has_type.label(class='label') }}
            <div class="field-body ml-4">
                <div class="control">
                    <label class="radio">
                        <input type="radio" name="has_type" value="draft">
                        草稿
                    </label>
                    <label class="radio">
                        <input checked type="radio" name="has_type" value="show">
                        发布
                    </label>
                </div>
            </div>
        </div>
        <div class="is-block">
            <div class="box has-background-light is-shadowless level">
                <button class=" is-danger button level-left">删除</button>
                <div class="level-right">
                    <a href="{{ url_for('admin.article') }}" class="button is-primary is-light mr-2">返回</a>
                    <input type="submit" value="保存" class=" button is-success">
                </div>
            </div>
        </div>

    </form>
{% endblock table_content %}
```
最后修改添加分类按钮的url即可：

路径：app/admin/templates/admin/article.html
```text
{% block button %}
    <div class="is-pulled-right">
        <a href="{{ url_for('admin.article_add') }}" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加文章</span> 
        </a>
    </div>
{% endblock button %}
```
## 实现修改博客内容
在app/admin/views.py中创建修改文章视图
```text
@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(
        title=post.title, desc=post.desc, 
        category_id=post.category.id, has_type=post.has_type.value,
        content=post.content, tags=tags
    )

    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id=int(form.category_id.data)
        post.content = form.content.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)
```
这里唯一需要注意的是在回显数据的时候多对多及一对多数据的回显需要特殊处理, 代码如下：

```text
post = Post.query.get(post_id)
tags = [tag.id for tag in post.tags]
form = PostForm(
    title=post.title, desc=post.desc, 
    category_id=post.category.id, has_type=post.has_type.value,
    content=post.content, tags=tags
)
```
其他的修改则和保存逻辑基本一致，大家多加练习即可掌握！

## 实现删除博客
在app/admin/views.py中创建删除视图
```text
@bp.route('/article/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_del(post_id):
    # 删除文章
    post = Post.query.get(post_id)
    if post:  
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}文章删除成功')
        return redirect(url_for('admin.article'))
```
在删除按钮上增加该url即可
路径： admin/templease/admin/article.html
```text
                        <a href="{{ url_for('admin.article_edit', post_id=post.id) }}" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="{{ url_for('admin.article_del', post_id=post.id) }}" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
```

最后在admin主页增加文章管理的url
```text
                    <ul class="menu-list">
                        <li><a class="{% if 'article' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.article') }}">文章管理</a></li>
                    </ul>
```
## 文章标签管理
在一些常见的博客网站我们一般看到的文章标签都是多对多关系，也就是一个文章可以对应多个标签，多个标签也可以对应多个文章，一般的操作逻辑是，在添加文章的时候选择已有的标签，如果没有符合的标签的话，可以自行添加标签！

这里我们现在目前的实现方案是选择了一种最为简单的方式，就是标签单独管理，添加文章时只做选择不做添加。

## 修改admin/forms.py中增加TagForm
```text
class TagForm(FlaskForm):
    # 标签表单
    name = StringField('标签', validators=[
        DataRequired(message="不能为空"),
        Length(max=128, message="不符合字数要求！")
    ])
```

## 创建标签的增删改查视图函数
路径： app/admin/views.py

```text
@bp.route('/tag')
@login_required
def tag():
    # 查看标签列表
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(page, per_page=10, error_out=False)
    tag_list = pagination.items
    return render_template('admin/tag.html', tag_list=tag_list, pagination=pagination)


@bp.route('/tag/add', methods=['GET', 'POST'])
@login_required
def tag_add():
    # 增加标签
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    # 修改标签
    tag = Tag.query.get(tag_id)
    form = TagForm(name=tag.name)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/del/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_del(tag_id):
    # 删除标签
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}删除成功')
        return redirect(url_for('admin.tag'))
```
## 修改admin/templates/admin/index.html
复制文章管理 为文章标签
```text
                    <ul class="menu-list">
                        <li><a class="{% if 'article' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.article') }}">文章管理</a></li>
                        <li><a class="{% if 'tag' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.tag') }}">文章标签</a></li>
                    </ul>
```

## 创建tag.html和tag_form.html
tag.html
```text
{% extends 'admin/index.html' %}    

{% block member %}
<div class="is-block">
    <div class=" is-pulled-left">
        <h1 class=" is-size-4">
            <span class="icon">
                <i class="mdi mdi-tag-outline"></i>
            </span>
            标签管理
        </h1>
    </div>

    {% block button %}
    <div class=" is-pulled-right">
        <a href="{{ url_for('admin.tag_add') }}" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加标签</span>
        </a>
    </div>
    {% endblock button %}
    <div class="is-clearfix"></div>
    <div class=" dropdown-divider"></div>

    <!-- 消息闪现 -->
    {% with messages = get_flashed_messages() %}
    <b-message type="is-success">
      {% if messages %}
      <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </b-message>
    {% endwith %}
</div>

{% block table_content %}
<div class="table-container">
    <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
            <tr>
              <th>ID</th>
              <th>标签名称</th>
              <th>发布日期</th>
              <th>操作</th>
            </tr>
        </thead>
        <tbody>

            {% for tag in tag_list %}       
            <tr>
                <td>{{ tag.id }}</td>
                <td>{{ tag.name }}</td>
                <td>{{ tag.add_date }}</td>
                <td>
                    <div class="tags">
                        <a href="{{ url_for('admin.tag_edit', tag_id=tag.id) }}" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="{{ url_for('admin.tag_del', tag_id=tag.id) }}" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<nav class="pagination is-small" role="navigation" aria-label="pagination">
    {% if pagination.has_prev %}
    <a href="{{ url_for('admin.tag') }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
    {% endif %}
    {% if pagination.has_next %}
    <a href="{{ url_for('admin.tag') }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
    {% endif %}

    <ul class="pagination-list">        
        {% for page in pagination.iter_pages() %}
            {% if page %} 
                {% if page != pagination.page %}
                <li>
                    <a href="{{ url_for('admin.tag') }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% else %}
                <li>
                    <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% endif %}
            {% else %}
                <span class=pagination-ellipsis>&hellip;</span>
            {% endif %}
        {% endfor %}

    </ul>
</nav>

{% endblock table_content %}
{% endblock member %}
```
## tag_form.html
```text
{% extends 'admin/category.html' %}

{% block button %}{% endblock button %}


{% block table_content %}
    <form action="" method="post" class="mt-4">
        {{ form.csrf_token }}
        <div class="field">
            {{ form.name.label(class='label') }}
            <div class="control">
                {{ form.name(class='input', placeholder='标签名称') }}
            </div>
        </div>

        <div class="is-block">
            <div class="box has-background-light is-shadowless level">
                <button class=" is-danger button level-left">删除</button>
                <div class="level-right">
                    <a href="{{ url_for('admin.tag') }}" class="button is-primary is-light mr-2">返回</a>
                    <input type="submit" value="保存" class=" button is-success">
                </div>
            </div>
        </div>
    </form>
{% endblock table_content %}
```
## 实现用户管理

通过上几节的功能实现，我们应该已经对flask_sqlalchemy的增删改查非常熟悉了，那么我们就来实现 最后一个用户管理的功能，用户管理功能部分内容，我们主要为大家展示如何实现flask的图片上传功能 以及用户密码的修改思路及方法！

## 创建用户列表视图
路径：app/admin/views.py
```text
@bp.route('/user')
@login_required
def user():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(-User.add_date).paginate(page=page, per_page=10, error_out=False)
    user_list = pagination.items
    return render_template('admin/user.html', user_list=user_list, pagination=pagination)
```
## 创建添加用户视图
在创建添加视图之前应该先要创建表单

在app/admin/forms.py中创建一个CreateUserForm的表单类
```text
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed

class CreateUserForm(FlaskForm):
    # 创建表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
        ])
    password = PasswordField('password', validators=[
        # DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
        ], description="修改用户信息时，留空则代表不修改！")
    avatar = FileField("avatar", validators=[
        # FileRequired(), 
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=2048000, message="不能大于2M")],
        description="大小不超过2M，仅支持jpg/png/gif格式，不选择则代表不修改")
    is_super_user = BooleanField("是否为管理员")
    is_active = BooleanField("是否活跃", default=True)
    is_staff = BooleanField("是否锁定")
```
这里我们将定义一个avatar的表单为文件表单FileField，这个类并不是wtforms提供的，而是flask_wtf为我们二次封装好的类，他帮我们分装好了两个验证类FileAllowed类来验证文件格式，FileSize来验证文件的大小，这样我们就可以不必须再去在视图中对这两个去额外验证，用法如代码所示，其中max_size的值是字节数，大家注意换算！

## 创建用户列表模板
路径：app/admin/user.html
```text
{% extends 'admin/index.html' %}    

{% block member %}
<div class="is-block">
    <div class=" is-pulled-left">
        <h1 class=" is-size-4">
            <span class="icon">
                <i class="mdi mdi-tag-outline"></i>
            </span>
            用户管理
        </h1>
    </div>

    {% block button %}
    <div class=" is-pulled-right">
        <a href="{{ url_for('admin.user_add') }}" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加用户</span>
        </a>
    </div>
    {% endblock button %}
    <div class="is-clearfix"></div>
    <div class=" dropdown-divider"></div>

    <!-- 消息闪现 -->
    {% with messages = get_flashed_messages() %}
    <b-message type="is-success">
      {% if messages %}
      <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </b-message>
    {% endwith %}
</div>

{% block table_content %}
<div class="table-container">
    <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
            <tr>
              <th>ID</th>
              <th>头像</th>
              <th>用户名</th>
              <th>管理员</th>
              <th>是否活跃</th>
              <th>是否锁定</th>
              <th>添加日期</th>
              <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for user in user_list %}       
            <tr>
                <td>{{ user.id }}</td>
                <td>
                    {% if user.avatar %}
                    <figure class="image is-48x48">
                        <img class="is-rounded" src="/admin/static/{{ user.avatar }}" alt="{{ user.username }}">
                    </figure>
                    {% else %}
                    -
                    {% endif %}
                </td>
                <td>{{ user.username }}</td>
                <td>
                    {% if user.is_super_user %}
                        <span class="icon has-text-success-dark">
                            <i class="mdi mdi-check"></i>
                        </span>
                    {% else %}
                        <span class="icon has-text-danger-dark">
                            <i class="mdi mdi-close"></i>
                        </span>
                    {% endif %}
                </td>
                <td>
                    {% if user.is_active %}
                        <span class="icon has-text-success-dark">
                            <i class="mdi mdi-check"></i>
                        </span>
                    {% else %}
                        <span class="icon has-text-danger-dark">
                            <i class="mdi mdi-close"></i>
                        </span>
                    {% endif %}
                </td>
                <td>
                    {% if user.is_staff %}
                        <span class="icon has-text-danger-dark">
                            <i class="mdi mdi-lock-outline"></i>
                        </span>
                    {% else %}
                        <span class="icon has-text-success-dark">
                            <i class="mdi mdi-lock-open-variant-outline"></i>
                        </span>
                    {% endif %}
                </td>
                <td>{{ user.add_date }}</td>
                <td>
                    <div class="tags">
                        <a href="{{ url_for('admin.user_edit', user_id=user.id) }}" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="{{ url_for('admin.user_del', user_id=user.id) }}" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<nav class="pagination is-small" role="navigation" aria-label="pagination">
    {% if pagination.has_prev %}
    <a href="{{ url_for('admin.user') }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
    {% endif %}
    {% if pagination.has_next %}
    <a href="{{ url_for('admin.user') }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
    {% endif %}

    <ul class="pagination-list">        
        {% for page in pagination.iter_pages() %}
            {% if page %} 
                {% if page != pagination.page %}
                <li>
                    <a href="{{ url_for('admin.user') }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% else %}
                <li>
                    <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% endif %}
            {% else %}
                <span class=pagination-ellipsis>&hellip;</span>
            {% endif %}
        {% endfor %}
    </ul>
</nav>
{% endblock table_content %}
{% endblock member %}
```


## 创建添加用户视图
```text
@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    # 查看文章列表
    # https://flask-wtf.readthedocs.io/en/1.0.x/form/#file-uploads
    form = CreateUserForm()
    if form.validate_on_submit():
        from .utils import upload_file_path
        f = form.avatar.data
        avatar_path, filename = upload_file_path('avatar', f)
        f.save(avatar_path)
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            avatar=f'avatar/{filename}',
            is_super_user=form.is_super_user.data,
            is_active=form.is_active.data,
            is_staff=form.is_staff.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}添加成功！')
        return redirect(url_for('admin.user'))
    return render_template('admin/user_form.html', form=form)
```

## 创建添加用户模板
创建app/admin/templates/admin/user_form.html
```text
{% extends 'admin/category.html' %}

{% block button %}{% endblock button %}


{% block table_content %}
    <form action="" method="post" class="mt-4" enctype="multipart/form-data">
        {{ form.csrf_token }}
        <div class="field">
            {{ form.username.label(class='label') }}
            <div class="control">
                {{ form.username(class='input', placeholder='用户名') }}
            </div>
        </div>
        <div class="field">
            {{ form.password.label(class='label') }}
            <div class="control">
                {{ form.password(class='input', placeholder='密码') }}
                <p class="help has-text-grey-light">
                    {{ form.password.description }}
                </p>
            </div>
        </div>
        <div class="field">
            {{ form.avatar.label(class='label') }}
            <div class="control">
                {{ form.avatar(class='input',  placeholder='头像') }}
                <p class="help has-text-grey-light">
                    {{ form.avatar.description }}
                </p>
            </div>
        </div>

        <div class="field">
            <label class="checkbox">
                {{ form.is_super_user }}
                {{ form.is_super_user.label }}
            </label>
        </div>
        <div class="field">
            <label class="checkbox">
                {{ form.is_active }}
                {{ form.is_active.label }}
            </label>
        </div>
        <div class="field">
            <label class="checkbox">
                {{ form.is_staff }}
                {{ form.is_staff.label }}
            </label>
        </div>
        <div class="is-block">
            <div class="box has-background-light is-shadowless level">
                <button class=" is-danger button level-left">删除</button>
                <div class="level-right">
                    <a href="{{ url_for('admin.user') }}" class="button is-primary is-light mr-2">返回</a>
                    <input type="submit" value="保存" class=" button is-success">
                </div>
            </div>
        </div>
    </form>
{% endblock table_content %} 
```

flask上传文件其实非常简单，他帮我们封装了一个save()方法，只需要用文件file.save(path),参数path就是文件的上传路径!

这段代码中我们引入了一个upload_file_path的方法，这个方法是我自己封装的一个小工具，用来判断上传的路径是否存在，不存在则创建，并对文件名进行了处理，把文件名中的中文给剔除掉并重命名！具体代码如下：
路径：app/admin/utils.py
```text
import os
import uuid
from RealProject.settings import BASE_DIR
from werkzeug.utils import secure_filename


def _file_path(directory_name):
    """判断该路径是否存在不存在则创建
    """
    file_path = BASE_DIR / f'app/admin/static/{directory_name}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path


def update_filename(f):
    """修改文件名
    """
    names = list(os.path.splitext(secure_filename(f.filename)))
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names)


def upload_file_path(directory_name, f):
    # 构造上传文件路径
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    return file_path / filename, filename

```
这几个函数的代码非常简单，都是python的基础知识，大家自行理解，其中参数directory_name是文件夹名称，可以自己定义，一个字符串，也可以是路径字符串， f则是文件对象！


## 创建修改用户视图
```text
@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    # 修改用户信息
    user = User.query.get(user_id)

    from .utils import upload_file_path
    form = CreateUserForm(
        username=user.username, 
        password=user.password,
        avatar=user.avatar,
        is_super_user=user.is_super_user,
        is_active=user.is_active,
        is_staff=user.is_staff 
    )
    form.password.default = f'{user.password}'

    if form.validate_on_submit():
        user.username = form.username.data
        if not form.password.data:
            user.password = user.password
        else:
            user.password = generate_password_hash(form.password.data)
        f = form.avatar.data
        if user.avatar == f:
            user.avatar = user.avatar
        else:
            avatar_path, filename = upload_file_path('avatar', f)
            f.save(avatar_path)
            user.avatar = f'avatar/{filename}'
        user.is_super_user = form.is_super_user.data
        user.is_active = form.is_active.data
        user.is_staff = form.is_staff.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.user'))
    return render_template('admin/user_form.html', form=form, user=user)
```
修改用户视图这块的逻辑与保存逻辑基本一致，要注意的地方是对密码和头像的修改，因为在我们使用表单PasswordField表单类的时候他默认不会回显到表单，那么密码表单默认在修改的时候即为空表单，此时我们就可以判断表单是否为空来判断用户是否要修改密码，因为密码我们做了加密处理，在数据库中存储的是密文，而不是明文，所以这里就得特殊处理！

修改密码逻辑代码：
```text
# 如果表单为空
if not form.password.data:
    # 密码不做任何修改原封保存
    user.password = user.password
else:
    # 不为空则获取表单值加密保存
    user.password = generate_password_hash(form.password.data)
```
头像这块处理的逻辑同样需要处理，可以判断表单值和修改用户的头像是否一致来处理，如果一样，说明未做任何修改，如果不同则执行上传图片操作，再替换头像表单中的值！

逻辑代码如下：
```text
f = form.avatar.data
if user.avatar == f:
    user.avatar = user.avatar
else:
    avatar_path, filename = upload_file_path('avatar', f)
    f.save(avatar_path)
    user.avatar = f'avatar/{filename}'
```
## 创建删除用户视图
```text
@bp.route('/user/del/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_del(user_id):
    # 删除标签
    user = User.query.get(user_id)
    if tag:
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username}删除成功')
        return redirect(url_for('admin.user'))
```
## 修改blog/templates/base.html中图标样式
```text
    <title>{% block title %}{% endblock title %}</title>
    <link rel="stylesheet" href="{{ url_for('blog.static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('blog.static', filename='css/buefy.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('blog.static', filename='css/materialdesignicons.min.css') }}">
    {% block extra_head_style %}{% endblock extra_head_style %}
```


最后在admin/templates/admin/index.html中增加用户管理url
```text
                    <ul class="menu-list">
                        <li><a class="{% if 'user' in request.path %}is-active{% endif %}"
                                href="{{ url_for('admin.user') }}">用户管理</a></li>
                        <li><a>修改密码</a></li>
                    </ul>
```

## 实现全站导航菜单及首页数据展示

## Flask上下文处理器
我们博客的设计是全站顶部菜单为通用菜单，调用的数据为文章的分类，那么如何将文章分类数据传递到每个页面的上下文呢？

为了将新变量自动注入模板的上下文中，Flask 中存在上下文处理器context_processor。上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：

用法为如下所示，这只是一个例子：

```text
@app.context_processor
def inject_user():
    return dict(user=g.user)
```
上面的上下文处理器使一个名为 user 的变量在模板中可用，其值为 g.user。这个例子不是很有趣，因为g无论如何都可以在模板中使用，但它给出了它是如何工作的。

变量不限于值;上下文处理器还可以使函数可用于模板（因为Python允许传递函数）：
```text
@app.context_processor
def utility_processor():
    def format_price(amount, currency="€"):
        return f"{amount:.2f}{currency}"
    return dict(format_price=format_price)
```
上面的上下文处理器使format_price函数可用于所有模板：

```text
{{ format_price(0.33) }}
```

您还可以将format_price构建为模板筛选器，但这演示了如何在上下文处理器中传递函数。

## 实现全站导航功能
知道了上下文处理器的用法，实现这个功能就非常简单了！

在RealProject目录的__init__.py中插入如下一个上下文回调函数
```text
def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)
```
这个函数通过limit()方法查询出前6个数据，并通过一个字典返回，之后我们还需要将该回调函数注册到app的工厂函数当中！

```text
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 省略部分代码

    # 全局上下文 
    app.context_processor(inject_category)
    return app
```
在app/blog/templates/base.html中循环查出我们返回的数据即可

```text
<!-- 导航 -->
{% block navbar %}     
<template>
    <b-navbar spaced shadow>
        <template #brand>
            <b-navbar-item>
                <img src="{{ url_for('blog.static', filename='img/logo.png') }}" alt="FlaskBlog">
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item href="/" 
                {% if request.path =='/' %}active {% endif %}>
                首页
            </b-navbar-item>

            <!-- 查询菜单数据 -->
            {% for cate in categorys %}
            <b-navbar-item href="#">
                {{ cate.name }}
            </b-navbar-item>
            {% endfor %}    
        </template>

        <!-- ...省略部分代码 -->
    </b-navbar>
</template>
{% endblock navbar %}
<!-- 导航 end -->
```

## 实现首页视图数据

在app/blog/views.py文件中的index首页视图函数中实现

```text
def index():
    """首页视图
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=9, error_out=False)
    post_list = pagination.items

    import random
    imgs = ['图一url', '图二url', '图三url']

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
        # post.img = random.choice(imgs)

    return render_template('index.html', posts=post_list, pagination=pagination)
```
这个视图函数中的查询逻辑在实现文章管理的时候已经实现过，这里唯一不同的区别就是我给这个返回数据新增了一个img的属性，因为在数据库我们没有设计文章形象图字段，我们用这种方式弥补，在imgs的列表中预设一些图片的url地址，之后随机抽取一个赋值给img属性，这样在模板中直接调用这个img属性就会获取到图片的url!

在app/blog/templates/base.html中替换相关循环数据

```text
<div class="columns is-multiline">
    {% for post in posts %}
    <div class="column is-4-fullhd is-6-desk">
        <div class="card">
            <div class="card-image">
                <figure class="image is-4by5">
                    <img src="{{ post.img }}"
                        alt="Placeholder image">
                </figure>
            </div>
            <div class="card-content">
                <div class="content">
                    <p class="title is-4"><a href="">{{ post.title }}</a> </p>
                    <p class="has-text-grey subtitle is-size-6"> 
                        {{ post.desc }}
                    </p>
                    <time class="has-text-grey" datetime="{{ post.add_date }}">{{ post.add_date }}</time>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```
最终效果： 

![img_6.png](img_6.png)


## 实现文章列表页及详情页

## 实现分类列表页
在设计数据库字段的时候，我们将分类与文章设置为一对多关系，一个分类下可以有多篇文章，那么导航栏通过上一节我们已经实现了，那么这一节我们就实现每个分类下的文章列表页！

在app/blog/views.py中实现分类页视图
```text
@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    # 分类页
    cate = Category.query.get(cate_id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.category_id == cate_id).paginate(page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('cate_list.html', cate=cate, post_list=post_list, cate_id=cate_id, pagination=pagination)
```
这个函数的逻辑也是在之前实现管理后台的时候多次实现，这里我们用了filter的查询方法根据url传进来的分类主键id来查询当前分类下的数据，并对其进行分页！

在app/blog/templates/中创建一个cate_list.html的模板文件
```text
{% extends 'base.html' %}

{% block title %}{{ cate.name }}{% endblock title %}

{% block hero %}{% endblock hero %}

{% block box %}
<div class="columns">
    <div class="column is-9" style="border-right:solid 1px #eee ;">
        <div class="box is-shadowless has-background-light">
            {% block breadcrumb %}
            <nav class="breadcrumb is-small" aria-label="breadcrumbs">
                <ul>
                <li><a href="/">首页</a></li>
                <li class="is-active"><a href="#" aria-current="page">{{ cate.name }}</a></li>
                </ul>
            </nav>
            {% endblock breadcrumb %}
        </div>

        {% block cate_box %}
        {% for post in post_list %}
            <div class="pl-2">
                <h1 class="is-size-4">
                    <a href="">{{ post.title }}</a>
                </h1>
                <p class="has-text-grey-light is-size-6 mt-1">
                    <span class="icon"><i class="mdi mdi-clipboard-text-clock-outline"></i></span>{{ post.add_date }}
                    <span class="icon"><i class="mdi mdi-shape-outline"></i></span>{{ post.category.name }}
                    <span class="icon"><i class="mdi mdi-tag-heart-outline"></i></span>{{ post.tags|join(',') }}
                </p>
                <div class="has-text-grey mt-1">{{ post.desc }}</div>
            </div>
            <div class=" dropdown-divider mb-3"></div>
        {% endfor %}
        {% block pagination %}
        <nav class="pagination is-small" role="navigation" aria-label="pagination">
            {% if pagination.has_prev %}
            <a href="{{ url_for('blog.cates', cate_id=cate.id ) }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
            {% endif %}
            {% if pagination.has_next %}
            <a href="{{ url_for('blog.cates', cate_id=cate.id) }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
            {% endif %}

            <ul class="pagination-list">        
                {% for page in pagination.iter_pages() %}
                    {% if page %} 
                        {% if page != pagination.page %}
                        <li>
                            <a href="{{ url_for('blog.cates', cate_id=cate.id) }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                        {% else %}
                        <li>
                            <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                        {% endif %}
                    {% else %}
                        <span class=pagination-ellipsis>&hellip;</span>
                    {% endif %}
                {% endfor %}

            </ul>
        </nav>
        {% endblock pagination %}
        {% endblock cate_box %}
    </div>
    <div class="column">
        asdas
    </div>
</div>
{% endblock box %}
```
## 修改base.html
```text
                            <!-- 查询菜单数据 -->
                            {% for cate in categorys %}
                            <b-navbar-item href="{{ url_for('blog.cates', cate_id=cate.id) }}">
                                {{ cate.name }}
                            </b-navbar-item>
                            {% endfor %}
                        </template>
```

该模板中我们查询出了刚才视图中返回的数据，并继承base.html实现了一个一本的样式！


## 实现文章详情页
在app/blog/views.py中实现文章详情页视图
```text
@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id, post_id):
    # 详情页
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)

    # 上一篇
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    # 下一篇
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    return render_template('detail.html', cate=cate, post=post, prev_post=prev_post, next_post=next_post)
```
这段代码不仅实现了文章详情页，还实现了上一篇及下一篇的功能！

通过url我们分别传入了分类cate_id以及当前文章post_id两个主键，之后根据这两个主键获取所属分类的及文章,代码如下：
```text
cate = Category.query.get(cate_id)
post = Post.query.get_or_404(post_id)
```
在这里我们同时实现了详情页的上一篇及下一篇的功能，根据当前文章的id来判断筛选出上一篇和下一篇！代码如下：
```text
# 上一篇
prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
# 下一篇
next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()
```
在app/blog/templates/中创建一个detail.html的模板文件
```text
{% extends 'cate_list.html' %}

{% block title %}
    {{ post.title }}
{% endblock title %}

{% block breadcrumb %}
    <nav class="breadcrumb is-small" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">首页</a></li>
            <li><a href="{{ url_for('blog.cates', cate_id=cate.id) }}">{{ cate.name }}</a></li>
            <li class="is-active"><a href="#" aria-current="page">{{ post.title }}</a></li>
        </ul>
    </nav>
{% endblock breadcrumb %}

{% block cate_box %}
<div class="pl-2">
    <h1 class="is-size-3">
        {{ post.title }}
    </h1>
    <p class="has-text-grey-light is-size-6 mt-1">
        <span class="icon"><i class="mdi mdi-clipboard-text-clock-outline"></i></span>{{ post.add_date }}
        <span class="icon"><i class="mdi mdi-shape-outline"></i></span>{{ post.category.name }}
        <span class="icon"><i class="mdi mdi-tag-heart-outline"></i></span>{{ post.tags|join(',') }}
    </p>
    <div class="content has-text-grey mt-1">{{ post.content|safe }}</div>
</div>

<hr>
<div class="level">
    <div class="level-left">
        {% if prev_post %}
            上一篇：<a href="{{ url_for('blog.detail', cate_id=prev_post.category.id, post_id=prev_post.id) }}">{{ prev_post.title }}</a>
        {% endif %}
    </div>
    <div class="level-right">
        {% if next_post %}
            下一篇：<a href="{{ url_for('blog.detail', cate_id=next_post.category.id, post_id=next_post.id) }}">{{ next_post.title }}</a>
        {% endif %}
    </div>
</div>
{% endblock cate_box %}
```

## 增加导航菜单中的url

路径： app/blog/templates/base.html

```text
{% for cate in categorys %}
    <b-navbar-item
        {% if cate.id == cate_id %}class="has-text-primary"{% endif %} 
        href="{{ url_for('blog.cates', cate_id=cate.id) }}">
        {{ cate.name }}
    </b-navbar-item>
{% endfor %}
```
## 首页文章url完善
路径： app/blog/templates/base.html
```text
{% for post in posts %}
<div class="column is-4-fullhd is-6-desk">
    <div class="card">
        <div class="card-image">
            <figure class="image is-4by5">
                <img src="{{ post.img }}" alt="Placeholder image">
            </figure>
        </div>
        <div class="card-content">
            <div class="content">
                <p class="title is-4"><a
                        href="{{ url_for('blog.detail', cate_id=post.category.id, post_id=post.id) }}">{{ post.title}}</a> </p>
                <p class="has-text-grey subtitle is-size-6">
                    {{ post.desc }}
                </p>
                <time class="has-text-grey" datetime="{{ post.add_date }}">{{ post.add_date }}</time>
            </div>
        </div>
    </div>
</div>
{% endfor %}
```
## 集成富文本编辑器Quill
为什么需要集成富文本编辑器？

一个博客最主要的功能是什么，那就是写作，如果不能对我们发布的内容进行排版美化，那么我们所发布的内容又有什么意义? 对于阅读者来说也是非常的不友好和不尊重，一篇排版精良的文章往往会让人赏心悦目，也会让读者爱上你的博客，所以富文本编辑器的使用就显得非常重要！

为什么选择富文本编辑器Quill?

大家可能会有疑问，市面上那么多富文本编辑器为什么选择他，首先是Quill富文本编辑器是一款开源的编辑器，它在 GitHub 上的 star 数名列前茅。体验下来，它的优势是轻量、兼容性强、支持的插件扩展丰富，需要用到什么额外功能时再去单独引入就好了。

此外，它还有适用于 Vue 和 React 的封装版本，无论你习惯用哪个前端框架，都能无差异地使用它。

## 集成Quill

集成Quill的思路是在新增文章时显示空白的富文本编辑器，并将编辑器的内容同步赋值给表单，在编辑文章时则必须回显内容到富文本编辑器并同步修改表单内容！

在app/admin/templates/admin/article_form.html中新增表单元素

引入富文本编辑器的样式css以及用来异步提交的axios.js
```text
{% extends 'admin/article.html' %}

{% block button %}{% endblock button %}
下面为新增内容
{% block extra_head_style %}
<link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
{% endblock extra_head_style %}
```

新增一个富文本容器id为editor的div
```text
        <div class="field">
            {{ form.content.label(class='label') }}
            <div class="control">
                {{ form.content(class='textarea', rows="10", placeholder='文章详情') }}
            </div>
            <!-- 富文本编辑器 -->
            <div id="editor" style="height: 500px;"></div>
        </div>
```
在本模板中的底部引入Quill的js文件
```text
{% endblock table_content %}

下面为新增内容：
{% block extra_foot_script %}
<!-- Include the Quill library -->
<script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
{% endblock extra_foot_script %}
```
配置quill富文本编辑器(在最后面增加一下内容)
```text
{% block vue_script %}
<script>
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike', 'link'],        // toggled buttons
        ['blockquote', 'code-block', 'image'],

        // [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction

        // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': [] }],
        [{ 'align': [] }],

        ['clean']                                         // remove formatting button
    ];
    var quill = new Quill('#editor', {
        // debug: 'info',
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow',
        placeholder: 'Compose an epic...',
        readOnly: false,
        formats: {}
    });


    var html = quill.container.firstChild.innerHTML;
    var content = document.querySelector("textarea[name='content']");

    // 隐藏表单
    content.setAttribute('style', 'display:none')
    // 监听富文本并同步到表单
    quill.on('text-change', function (delta, oldDelta, source) {
        content.innerHTML = quill.container.firstChild.innerHTML;
    });

    // 回显内容
    quill.pasteHTML(content.value)

    // 上传图片方法
    var showImageUI = function(){
        var fileInput = this.container.querySelector('input.ql-image[type=file]');
        if (fileInput == null) {
            // 通过js方式构造一个上传表单
            fileInput = document.createElement('input');
            fileInput.setAttribute('type', 'file');
            fileInput.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
            fileInput.classList.add('ql-image');

            // 监听change事件
            fileInput.addEventListener('change', function () {
                if (fileInput.files != null && fileInput.files[0] != null) {
                    const formData = new FormData();
                    formData.append('upload', fileInput.files[0]);
                    axios({
                        url:'{{ url_for("admin.upload") }}',
                        method:'post',
                        data:formData,
                        headers:{'content-type': 'multipart/form-data'},
                    }).then(res => {
                        // 返回错误提示
                        if (res.data.code == 'err'){
                            alert(res.data.message)
                            return
                        }
                        // 设置图片回显到富文本编辑器
                        var range = quill.getSelection(true);
                        quill.insertEmbed(range.index, 'image', res.data.url);
                        quill.setSelection(range.index + 1);
                    }).catch(err => {
                        console.log(err)
                    })
                }
            });
            this.container.appendChild(fileInput);
        }
        fileInput.click();
    }

    // 上传图片
    var toolbar = quill.getModule('toolbar');
    toolbar.addHandler('image', showImageUI);

</script>
{% endblock vue_script %}
```
本段代码不会过多的去解释，相关内容可参考Quill的文档！

toolbarOptions变量为配置富文本编辑器的菜单项！

quill变量是初始化了一个富文本编辑器的对象

下边这段代码则是获取富文本的输入值及表单，监听富文本编辑器的text-change事件，并同步赋值给表单！

之后再将表单值回显到富文本编辑器，这个主要用来在编辑文章时回显内容！

```text
var html = quill.container.firstChild.innerHTML;
var content = document.querySelector("textarea[name='content']");

// 隐藏表单
content.setAttribute('style', 'display:none')
// 监听富文本并同步到表单
quill.on('text-change', function (delta, oldDelta, source) {
    content.innerHTML = quill.container.firstChild.innerHTML;
});

// 回显内容
quill.pasteHTML(content.value)
```
上传图片配置
```text
// 上传图片
var toolbar = quill.getModule('toolbar');
toolbar.addHandler('image', showImageUI);
```
这是向上传图片表单自定义一个上传方法showImageUI，这个方法则是上传图片的全部前端内容，当然还必须实现一个上传表单的后端接口，也就是axios中通过post提交的那个接口url！

## 实现后端图片上传接口
路径：app/admin/views.py
```text
@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    # 上传图片
    if request.method == 'POST':
        f = request.files.get('upload')
        file_size = len(f.read())
        f.seek(0)  # reset cursor position to beginning of file

        if file_size > 2048000:  # 限制上传大小为2M
            return {
                'code':'err',
                'message': '文件超过限制2048000字节',
            }
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {
            'code':'ok',
            'url':f'/admin/static/upload/{filename}'
        }
```
这段代码后端接口最主要的上传方法及验证方法我们在上传用户头像的章节已经讲过，这里我们只是复用了哪里的方法！
至此，我们的富文本编辑器就集成成功了！


## 实现侧边栏文章归档及标签
按照正常的博客网站布局，一般都会存在侧边栏，侧边栏比较常见的几个模块分别是 搜索、最新文章、文章归档、标签等！该教程会带大家实现这四个模块！

按照当前项目的布局，我们的侧边栏仅在blog应用中的页面展示，也就是博客的列列表页和详情页展示，那么这个视图是通过blog中的蓝图绑定的，因此我们在左侧边栏的时候只需要针对这个应用即可！

## 实现文章归档功能
在app/blog/views.py中通过博客的蓝图注入上下文,代码如下
```text
@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])

    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info', 'is-warning']

    return dict(dates=dates, tags=tags)
```
首先我们这里选择按月归档的方式，也就是把每个月的文章归类到一起，那么我们就必须先把年月查询显示到侧边栏，代码如下：
```text
posts = Post.query.order_by(Post.add_date)
dates = set([post.add_date.strftime("%Y年%m月") for post in posts])
```
首先查询出所有的文章并按照发布时间倒叙排列，也就是最新发布的文章在最前边，之后再提取出每篇文章的发布日期的年月，使用strftime方法格式化成我们需要的格式，并使用set简单去重，并返回到上下文！

## 实现文章归档的详情视图
路径： app/blog/views.py
```text
@bp.route('/category/<string:date>')
def archive(date):
    # 归档页
    import re
    # 正则匹配年月
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)

    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    # 根据年月获取数据
    archive_posts = Post.query.filter(and_(extract('year', Post.add_date) == int(dates[0]), extract('month', Post.add_date) == int(dates[1])))
    # 对数据进行分页
    pagination = archive_posts.paginate(page=page, per_page=10, error_out=False)
    return render_template('archive.html', post_list=pagination.items,  pagination=pagination, date=date)
```
详情视图我们通过url传递进来要访问的日期，并通过正则表达式提取出年和月,代码如下：
```text
import re
# 正则匹配年月
regex = re.compile(r'\d{4}|\d{2}')
dates = regex.findall(date)
```
下边这段代码引入了sqlalchemy提供extract, and_两个方法，extract用来提取某个字段的值，and_实现两个并且的关系，然后根据正则获取的 年月匹配查询出当月的文章！

```text
from sqlalchemy import extract, and_, or_
archive_posts = Post.query.filter(and_(extract('year', Post.add_date) == int(dates[0]), extract('month', Post.add_date) == int(dates[1])))
```
其他代码都是在之前的章节中多次使用，大家自行理解！

创建归档页模板，在app/blog/templates/中创建archive.html,代码如下：

```text
{% extends 'cate_list.html' %}

{% block title %}{{ date }}的文章归档 {% endblock title %}

{% block hero %}{% endblock hero %}

{% block breadcrumb %}
    <nav class="breadcrumb is-small" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">首页</a></li>
            <li class="is-active"><a href="#" aria-current="page">{{ date }}的归档</a></li>
        </ul>
    </nav>
{% endblock breadcrumb %}

{% block pagination %}
    <nav class="pagination is-small" role="navigation" aria-label="pagination">
        {% if pagination.has_prev %}
            <a href="{{ url_for('blog.archive', date=date ) }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
        {% endif %}
        {% if pagination.has_next %}
            <a href="{{ url_for('blog.archive', date=date) }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
        {% endif %}

        <ul class="pagination-list">        
            {% for page in pagination.iter_pages() %}
                {% if page %} 
                    {% if page != pagination.page %}
                        <li>
                            <a href="{{ url_for('blog.archive', date=date) }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                    {% endif %}
                {% else %}
                    <span class=pagination-ellipsis>&hellip;</span>
                {% endif %}
                {% endfor %}
            </ul>
        </nav>
{% endblock pagination %}
```

## 实现标签详情视图
```text
@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    # 标签页
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)
```
创建标签页模板，在app/blog/templates/中创建tags.html,代码如下：

```text
{% extends 'cate_list.html' %}

{% block title %}{{ tag }} {% endblock title %}

{% block hero %}{% endblock hero %}

{% block breadcrumb %}
    <nav class="breadcrumb is-small" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">首页</a></li>
            <li class="is-active"><a href="#" aria-current="page">{{ tag }}</a></li>
        </ul>
    </nav>
{% endblock breadcrumb %}

{% block pagination %}
{% endblock pagination %}
```

## 模板中新增侧边栏模块
在app/blog/templates/cate_list.html中我们预留的右侧块中新增如下代码
````text
    <div class="box is-shadowless" style="border:solid 1px #eee ;">
        <h1 class="is-size-6 icon-text">
            <span class="icon"><i class="mdi mdi-calendar-month-outline"></i></span>
            归档
        </h1>
        <div class=" dropdown-divider"></div>
        <ul>
            {% for date in dates %}
            <li class="pl-2"><a href="{{ url_for('blog.archive', date=date) }}">{{ date }}</a></li>
            <div class="dropdown-divider"></div>
            {% endfor %}
        </ul>
        <h1 class="is-size-6 icon-text">
            <span class="icon"><i class="mdi mdi-tag-multiple-outline"></i></span>
            标签
        </h1>
        <div class=" dropdown-divider"></div>
        <div class="tags">
                {% for tag in tags %}
                <a class="tag {{ tag.style|random() }}" href="{{ url_for('blog.tags', tag_id=tag.id) }}">{{ tag.name }}</a>
                {% endfor %}
            </div>
    </div>
````
## 实现侧边栏最新文章及搜索

## 实现最新文章模块
这个就非常简单了，只需要将将最新文章传入blog的上下文中即可
在app/blog/views.py的inject_archive函数中新增代码如下：

```text
@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(-Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts]
    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info',
                     'is-warning']

    # 最新文章
    new_posts = posts.limit(6)
    return dict(dates=dates, tags=tags, new_posts=new_posts)
```

在app/blog/templates/cate_list.html的侧边栏新增如下代码：
```text
<div class="box is-shadowless" style="border:solid 1px #eee ;">
    <h1 class="is-size-6 icon-text">
        <span class="icon"><i class="mdi mdi-calendar-month-outline"></i></span>
        最新文章
    </h1>
    <div class=" dropdown-divider"></div>
    <ul>
        {% for post in new_posts %}
        <li class="pl-2">
            <span class=" has-text-grey-light">{{ loop.index }}.</span> 
            <a href="{{ url_for('blog.detail', cate_id=post.category.id, post_id=post.id) }}">{{ post.title }}</a>
        </li>
        <div class="dropdown-divider"></div>
        {% endfor %}
    </ul>
</div>
```
## 实现搜索模块
搜索模块的逻辑是通过get请求把关键字传给后端，后端通过filter方法自配合字段的like方法进行模糊匹配，返回结果即可！
```text
@bp.route('/search')
def search():
    # 搜索视图
    words = request.args.get('words', '', type=str)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.title.like("%"+words+"%")).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('search.html', post_list=post_list, words=words, pagination=pagination)
```

在app/blog/templates/cate_list.html的侧边栏新增如下代码：
```text
<div class="box is-shadowless" style="border:solid 1px #eee ;">
    <h1 class="is-size-6 icon-text">
        <span class="icon"><i class="mdi mdi-search-web"></i></span>
        搜索
    </h1>
    <div class=" dropdown-divider"></div>
    <form action="{{ url_for('blog.search') }}" method="get">
        <div class="field has-addons">
            <div class="control">
            <input class="input" type="search" value="{{ words }}" name="words" placeholder="请输入关键字">
            </div>
            <div class="control">
            <input type="submit" value="Search" class="button is-info">
            </div>
        </div>
    </form>
</div>
```
在app/blog/templates/中创建search.html,代码如下：
```text
{% extends 'cate_list.html' %}

{% block title %}{{ words }}的搜索结果 {% endblock title %}

{% block hero %}{% endblock hero %}

{% block breadcrumb %}
    <nav class="breadcrumb is-small" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">首页</a></li>
            <li class="is-active"><a href="#" aria-current="page">{{ words }}</a></li>
        </ul>
    </nav>
{% endblock breadcrumb %}

{% block pagination %}
    <nav class="pagination is-small" role="navigation" aria-label="pagination">
        {% if pagination.has_prev %}
            <a href="{{ url_for('blog.search') }}?page={{ pagination.prev_num }}&words={{ words }}" class="pagination-previous" title="This is the first page">Previous</a>
        {% endif %}
        {% if pagination.has_next %}
            <a href="{{ url_for('blog.search') }}?page={{ pagination.next_num }}&words={{ words }}" class="pagination-next">Next page</a>
        {% endif %}

        <ul class="pagination-list">        
            {% for page in pagination.iter_pages() %}
                {% if page %} 
                    {% if page != pagination.page %}
                        <li>
                            <a href="{{ url_for('blog.search') }}?page={{ page }}&words={{ words }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                    {% endif %}
                {% else %}
                    <span class=pagination-ellipsis>&hellip;</span>
                {% endif %}
                {% endfor %}
            </ul>
        </nav>
{% endblock pagination %}
```

因侧边栏操作比较多，总结下cate_list.html中的侧边栏顺序，整体的cate_list.html如下：
```text
{% extends 'base.html' %}

{% block title %}{{ cate.name }}{% endblock title %}

{% block hero %}{% endblock hero %}

{% block box %}
<div class="columns">
    <div class="column is-9" style="border-right:solid 1px #eee ;">
        <div class="box is-shadowless has-background-light">
            {% block breadcrumb %}
            <nav class="breadcrumb is-small" aria-label="breadcrumbs">
                <ul>
                <li><a href="/">首页</a></li>
                <li class="is-active"><a href="#" aria-current="page">{{ cate.name }}</a></li>
                </ul>
            </nav>
            {% endblock breadcrumb %}
        </div>

        {% block cate_box %}
        {% for post in post_list %}
            <div class="pl-2">
                <h1 class="is-size-4">
                    <a href="{{ url_for('blog.detail', cate_id=post.category.id, post_id=post.id) }}">{{ post.title }}</a>
                </h1>
                <p class="has-text-grey-light is-size-6 mt-1">
                    <span class="icon"><i class="mdi mdi-clipboard-text-clock-outline"></i></span>{{ post.add_date }}
                    <span class="icon"><i class="mdi mdi-shape-outline"></i></span>{{ post.category.name }}
                    <span class="icon"><i class="mdi mdi-tag-heart-outline"></i></span>{{ post.tags|join(',') }}
                </p>
                <div class="has-text-grey mt-1">{{ post.desc }}</div>
            </div>
            <div class=" dropdown-divider mb-3"></div>
        {% endfor %}
        {% block pagination %}
        <nav class="pagination is-small" role="navigation" aria-label="pagination">
            {% if pagination.has_prev %}
            <a href="{{ url_for('blog.cates', cate_id=cate.id ) }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
            {% endif %}
            {% if pagination.has_next %}
            <a href="{{ url_for('blog.cates', cate_id=cate.id) }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
            {% endif %}

            <ul class="pagination-list">
                {% for page in pagination.iter_pages() %}
                    {% if page %}
                        {% if page != pagination.page %}
                        <li>
                            <a href="{{ url_for('blog.cates', cate_id=cate.id) }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                        {% else %}
                        <li>
                            <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                        </li>
                        {% endif %}
                    {% else %}
                        <span class=pagination-ellipsis>&hellip;</span>
                    {% endif %}
                {% endfor %}

            </ul>
        </nav>
        {% endblock pagination %}
        {% endblock cate_box %}
    </div>

    <div class="box is-shadowless" style="border:solid 1px #eee ;">
        <!--搜索-->
        <h1 class="is-size-6 icon-text">
            <span class="icon"><i class="mdi mdi-search-web"></i></span>
            搜索
        </h1>
        <div class=" dropdown-divider"></div>
        <form action="{{ url_for('blog.search') }}" method="get">
            <div class="field has-addons">
                <div class="control">
                <input class="input" type="search" value="{{ words }}" name="words" placeholder="请输入关键字">
                </div>
                <div class="control">
                <input type="submit" value="Search" class="button is-info">
                </div>
            </div>
        </form>

        <!--归档-->
        <h1 class="is-size-6 icon-text">
            <span class="icon"><i class="mdi mdi-calendar-month-outline"></i></span>
            归档
        </h1>
        <div class=" dropdown-divider"></div>
        <ul>
            {% for date in dates %}
            <li class="pl-2"><a href="{{ url_for('blog.archive', date=date) }}">{{ date }}</a></li>
            <div class="dropdown-divider"></div>
            {% endfor %}
        </ul>

        <!--最新文章-->
        <h1 class="is-size-6 icon-text">
        <span class="icon"><i class="mdi mdi-calendar-month-outline"></i></span>
        最新文章
    </h1>
        <div class=" dropdown-divider"></div>
        <ul>
        {% for post in new_posts %}
        <li class="pl-2">
            <span class=" has-text-grey-light">{{ loop.index }}.</span>
            <a href="{{ url_for('blog.detail', cate_id=post.category.id, post_id=post.id) }}">{{ post.title }}</a>
        </li>
        <div class="dropdown-divider"></div>
        {% endfor %}
    </ul>
                <!--标签-->
        <h1 class="is-size-6 icon-text">
            <span class="icon"><i class="mdi mdi-tag-multiple-outline"></i></span>
            标签
        </h1>
        <div class=" dropdown-divider"></div>
        <div class="tags">
                {% for tag in tags %}
                <a class="tag {{ tag.style|random() }}" href="{{ url_for('blog.tags', tag_id=tag.id) }}">{{ tag.name }}</a>
                {% endfor %}
            </div>

    </div>
</div>
{% endblock box %}
```

## 实现个人中心及权限管理

## 实现权限管理
在管理后台中比较有名的管理权限模型一般遵循RABC模型去实现，如果这部分内容展开讲的话，那堪比另外一个教程了，那么我们的博客非常简单，就以最简单的方式实现权限的管理，也给大家提供了一个flask权限配置的一个思路！

我们的用户目前就分类两类，一类是超级管理员，一类是普通用户，对于超级管理员拥有所有权限，可以访问网站的任何url，那么普通用户也就是注册登录的用户，则除了公开的url外只能访问授权的url，这个权限根据url去实现，控制的比较粗糙，但足以说明问题！

在app/auth/views/auth.py中的load_logged_in_user方法中注入权限标识,代码如下：
```text
@bp.before_app_request
def load_logged_in_user():
    # 每个请求之前都会去session中查看user_id来获取用户

    # 注册用户即非管理员用户允许登录后查看的url
    urls = ['/auth/']

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = auth.User.query.get(int(user_id))

        # 权限判断
        if g.user.is_super_user and g.user.is_active:
            g.user.has_perm = 1
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
            g.user.has_perm = 1
        else:
            g.user.has_perm = 0
```
这个函数使用了装饰器方法before_app_request，我们知道这个装饰器的作用是在访问每个url之前去检查用户是否登陆，这个在登录注册那两个章节我们有讲到，根据用户的模型设计我们可以判断is_super_user字段的值去区分是否为管理员还是普通用户，来返回权限标识!

```text
urls = ['/auth/']

 # 权限判断
if g.user.is_super_user and g.user.is_active:
    g.user.has_perm = 1
elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
    g.user.has_perm = 1
else:
    g.user.has_perm = 0
```
通过g对象给user挂载了一个has_perm的标识，通过他的返回值确认是否有访问urls列表中url的权限

之后在login_required的装饰器函数中进行权限判断，代码如下：

```text
def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # 给登录url添加一个记录上次访问的url参数，并跳转
            redirect_to = f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
        # 登录成功后对权限进行判断处理
        if g.user.has_perm:
            pass
        else:
            return '<h1>无权限查看！</h1>'
        return view(**kwargs)
    return wrapped_view
```
如果没有访问权限，我们直接给他返回了无权限查看的一个提示，配置完这些之后我们就可以去试着更换不同的用户访问管理后台的url试下，并在urls列表中增加url向用户赋予相关的url访问权限！

## 实现个人中心
个人中心不同于管理后台，个人中心普通用户可以访问，而超级管理员则可以访问个人中心和管理后台，个人中心我们一般用来记录当前登录用户的个人信息，提供当前用户修改自己的信息或查看自己收藏内容或留言内容或和自己相关的一些内容，当然这里的收藏及评论留言功能本教程并没有去实现，但所用到的知识点都是我们本教程中所提到的，所以如果大家需要这些功能，这些功能就留给大家去完成，以检验自己的学习成果！
在app/auth/views/auth.py中实现个人中心函数视图

```text
@bp.route('/')
@login_required
def userinfo():
    # 用户中心
    return render_template('userinfo.html')
```
在app/auth/templates/中创建个人中心模板userinfo.html
```text
{% extends 'admin/index.html' %}

{% block menus %}
<aside class="menu">
    <p class="menu-label">
        个人中心
    </p>
    <ul class="menu-list">
        <li><a class="{% if request.path == '/auth/' %}is-active{% endif %}"
                href="{{ url_for('auth.userinfo') }}">个人信息</a></li>
        <li>
            <a class="" href="">我的收藏</a>
        </li>
        <li>
            <a class="" href="">我的评论</a>
        </li>
    </ul>
</aside>
{% endblock menus %}

{% block member %}
<template>
    <b-tabs>
        <b-tab-item label="个人信息" icon="account-outline">

            <div class="columns is-mobile" style="border-bottom: #ededed solid 1px; padding-bottom: 1rem">
                <div class="column is-narrow">
                    <figure class="image is-96x96">
                        <img class="is-rounded" src="/admin/static/{{ g.user['avatar'] }}">
                    </figure>
                </div>
                <div class="column is-narrow">
                    <div style="padding-top: 1.5rem;">
                        <h1 class="title is-size-4">{{ g.user['username'] }}</h1>
                        <p class="subtitle is-size-6">暂未设置个性签名</p>
                    </div>
                </div>
                <div class="column is-narrow-mobile">
                    <a class=" button is-light is-pulled-right" href="" style="margin-top: 1.8rem">修改信息</a>
                </div>
            </div>

            <div class="columns" style="padding:1rem 0; ">
                <div class="column is-2">
                    <p>个人信息</p>
                </div>
                <div class="column">
                    <div class="columns is-mobile" style="border-bottom: #ededed solid 1px">
                        <div class="column is-2">
                            <span class=" has-text-grey-light">用户名</span>
                        </div>
                        <div class="column is-narrow">
                            <span class=" has-text-black-ter">{{ g.user['username'] }}</span>
                        </div>
                    </div>
                    <div class="columns is-mobile" style="border-bottom: #ededed solid 1px">
                        <div class="column is-2">
                            <span class=" has-text-grey-light">性别</span>
                        </div>
                        <div class="column is-narrow">
                            <span class=" has-text-black-ter">暂未设置</span>
                        </div>

                    </div>
                    <div class="columns is-mobile" style="border-bottom: #ededed solid 1px">
                        <div class="column is-2">
                            <span class=" has-text-grey-light">邮箱</span>
                        </div>
                        <div class="column is-narrow">
                            <span class=" has-text-black-ter">asdas@qq.com</span>
                        </div>

                    </div>

                    <div class="columns is-mobile" style="border-bottom: #ededed solid 1px">
                        <div class="column is-2">
                            <span class=" has-text-grey-light">地址</span>
                        </div>
                        <div class="column is-narrow">
                            <span class=" has-text-black-ter">暂未添加地址</span>
                        </div>

                    </div>
                </div>
            </div>

            <div class="columns" style="padding:1rem 0; ">
                <div class="column is-2">
                    <p>个人简介</p>
                </div>
                <div class="column">
                    <div class="content">

                        暂未设置

                    </div>
                </div>
            </div>

        </b-tab-item>
    </b-tabs>
</template>
{% endblock member %}
```
在 admin/templates/admin/index.html中修改内容，完整内容如下：
```text
{% extends 'base.html' %}

{% block title %}
{{ g.user['username'] }}-个人中心
{% endblock title %}

{% block hero %}{% endblock hero %}

{% block box %}
<div class="columns">
    <div class="column is-2">
        <div class="card is-shadowless" style="border-right:solid 1px #eee">
            <div class="card-content">
                {% block menus %}
                <aside class="menu">
                    <p class="menu-label">
                        仪表板
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if request.path == '/admin/' %}is-active{% endif %}"
                            href="{{ url_for('admin.index') }}">主页</a></li>
                        <!-- <li><a>Customers</a></li> -->
                    </ul>
                    <p class="menu-label">
                        博客分类
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if 'category' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.category') }}">分类管理</a></li>
                    </ul>
                    <p class="menu-label">
                        文章管理
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if 'article' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.article') }}">文章管理</a></li>
                        <li><a class="{% if 'tag' in request.path %}is-active{% endif %}"
                               href="{{ url_for('admin.tag') }}">文章标签</a></li>
                    </ul>
                    <p class="menu-label">
                        用户管理
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if 'user' in request.path %}is-active{% endif %}"
                                href="{{ url_for('admin.user') }}">用户管理</a></li>
                        <li><a>修改密码</a></li>
                    </ul>
                </aside>
                {% endblock menus %}
            </div>
        </div>
    </div>
    <div class="column">
        {% block member %}
        <div class="tile is-ancestor">
            <div class="tile is-parent">
                <article class="tile is-child notification is-info is-light">
                    <div class="content">
                        <p class="title">100</p>
                        <p class="subtitle">文章数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-success is-light">
                    <div class="content">
                        <p class="title">50</p>
                        <p class="subtitle">用户数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-warning is-light">
                    <div class="content">
                        <p class="title">150</p>
                        <p class="subtitle">评论数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
        </div>
        {% endblock member %}
    </div>
</div>
{% endblock box %}
```
最后，我们去修改下导航栏的个人中心按钮，让管理员显示进入管理后台的入口，普通用户只能看见个人中心的入口！

在app/blog/templates/base.html中修改代码如下：
```text
{% if g.user.is_super_user %}
    <a class="button is-success" href="{{ url_for('admin.index') }}">管理后台</a>
{% else %}
    <a class="button is-success" href="{{ url_for('auth.userinfo') }}">个人中心</a>
{% endif %}
```

## 设置Banner
路径： app/admin/models.py
```text
from datetime import datetime, timedelta
from RealProject import db


class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, ) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # 更新时间


class Banner(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(300), nullable=True)

    def __repr__(self) -> str:
        return f'{self.id}=>{self.img}'
```

注册到工厂函数中
```text
    # 注册数据库模型
    from app.blog import models
    from app.auth.models import auth
    from app.admin.models import Banner
```
并且同步到数据库中
```text
$env:FLASK_APP = "RealProject"
$env:FLASK_ENV = "development"
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db init
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db migrate
E:\pythonproject\FlaskBlog\venv\Scripts\flask.exe db upgrade
```
在admin/forms.py中添加BannerForm校验
```text
class BannerForm(FlaskForm):
    # banner表单
    img = FileField("Banner图", validators=[
        # FileRequired(), 
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=3 * 1024 * 1000, message="不能大于3M")],
                    description="大小不超过3M，仅支持jpg/png/gif格式，不选择则代表不修改, 尺寸比例：3:1")

    desc = StringField('描述', validators=[
        # DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])

    url = URLField("Url", validators=[
        URL(require_tld=False, message="请输入正确的url"),
        Length(max=300, message="不符合字数要求！")])
```


在admin/views.py中新增视图函数
```text
@bp.route('/banner')
@login_required
def banner():
    # banner列表
    from .models import Banner
    banners = Banner.query.all()
    return render_template('admin/banner.html', banners=banners)


@bp.route('/banner/add', methods=['GET', 'POST'])
@login_required
def banner_add():
    # banner添加
    from .forms import BannerForm
    form = BannerForm()
    if form.validate_on_submit():
        from .utils import upload_file_path
        f = form.img.data
        img_path, filename = upload_file_path('banner', f)
        f.save(img_path)
        banner = Banner(
            img=f'banner/{filename}',
            desc=form.desc.data,
            url=form.url.data
        )
        db.session.add(banner)
        db.session.commit()
        flash('banner图新增成功')
        return redirect(url_for('admin.banner'))
    return render_template('admin/banner_form.html', form=form)


@bp.route('/banner/edit/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def banner_edit(banner_id):
    # banner修改
    from .forms import BannerForm
    banner = Banner.query.get(banner_id)
    form = BannerForm(img=banner.img, desc=banner.desc, url=banner.url)
    if form.validate_on_submit():
        f = form.img.data
        if banner.img == f:
            banner.img = banner.img
        else:
            from .utils import upload_file_path
            img_path, filename = upload_file_path('banner', f)
            f.save(img_path)
            banner.img = f'banner/{filename}'
        banner.desc = form.desc.data
        banner.url = form.url.data
        return redirect(url_for('admin.banner'))
    return render_template('admin/banner_form.html', form=form, banner=banner)


@bp.route('/banner/del/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def banner_del(banner_id):
    # banner列表
    banner = Banner.query.get(banner_id)
    if banner:
        db.session.delete(banner)
        db.session.commit()
        flash(f'{banner.img}删除成功')
        return redirect(url_for('admin.banner'))


```


banner.html
```text
{% extends 'admin/index.html' %}

{% block member %}
<div class="is-block">
    <div class=" is-pulled-left">
        <h1 class=" is-size-4">
            <span class="icon">
                <i class="mdi mdi-image-multiple"></i>
            </span>
            Banner管理
        </h1>
    </div>
    
    {% block button %}
    <div class=" is-pulled-right">
        <a href="{{ url_for('admin.banner_add') }}" class=" button is-primary is-light">
            <span class="icon"><i class="mdi mdi-plus-thick"></i></span>
            <span>添加轮播图</span>
        </a>
    </div>
    {% endblock button %}
    <div class="is-clearfix"></div>
    <div class=" dropdown-divider"></div>

    <!-- 消息闪现 -->
    {% with messages = get_flashed_messages() %}
    <b-message type="is-success">
      {% if messages %}
      <ul class=flashes>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </b-message>
    {% endwith %}
    <!-- 表单验证 -->
    {% if form and form.errors %}
    <b-message type="is-danger">
    <ul class="errors">
        {% for error, v in form.errors.items() %}
            <li>{{ error }}：{{ v[0] }}</li>
        {% endfor %}
    </ul>
    </b-message>
    {% endif %}
</div>

{% block table_content %}
<div class="table-container">
    <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
            <tr>
              <th>ID</th>
              <th>轮播图</th>
              <th>Url</th>
              <th>描述</th>
              <th>发布日期</th>
              <th>操作</th>
            </tr>
        </thead>
        <tbody>
            
            {% for banner in banners %}       
            <tr>
                <td>{{ banner.id }}</td>
                <td>
                    <figure class="image is-16by9">
                        <img src="/admin/static/{{ banner.img }}">
                    </figure>
                </td>
                <td>{{ banner.url }}</td>
                <td>{{ banner.desc }}</td>
                <td>{{ banner.add_date }}</td>
                <td>
                    <div class="tags">
                        <a href="{{ url_for('admin.banner_edit', banner_id=banner.id) }}" class="tag is-success is-light">
                            <span class="icon">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </span>
                            编辑
                        </a>
                        <a href="{{ url_for('admin.banner_del', banner_id=banner.id) }}" class="tag is-danger is-light">
                            <span class="icon">
                                <i class="mdi mdi-trash-can-outline"></i>
                            </span>
                            删除
                        </a>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% endblock table_content %}
{% endblock member %}
```

banner_form.html
```text
{% extends 'admin/banner.html' %}

{% block button %}{% endblock button %}


{% block table_content %}
    <form action="" method="post" class="mt-4" enctype="multipart/form-data">
        {{ form.csrf_token }}
        <div class="field">
            {{ form.img.label(class='label') }}
            <div class="control">
                <b-field class="file">
                    <b-upload v-model="file" name="img" expanded>
                      <a class="button is-primary is-fullwidth">
                        <b-icon icon="upload"></b-icon>
                        <span>{$ file.name || "{% if banner %}{{ banner.img }}{% else %}Click to upload{% endif %}" $}</span>
                      </a>
                    </b-upload>
                </b-field>
                <p class="help has-text-grey-light">
                    {{ form.img.description }}
                </p>
            </div>
        </div>
        <div class="field">
            {{ form.url.label(class='label') }}
            <div class="control">
                {{ form.url(class='input', placeholder='url') }}
                <p class="help has-text-grey-light">
                    {{ form.url.description }}
                </p>
            </div>
        </div>
        <div class="field">
            {{ form.desc.label(class='label') }}
            <div class="control">
                {{ form.desc(class='input',  placeholder='描述') }}
                <p class="help has-text-grey-light">
                    {{ form.desc.description }}
                </p>
            </div>
        </div>
        
        <div class="is-block">
            <div class="box has-background-light is-shadowless level">
                <button class=" is-danger button level-left">删除</button>
                <div class="level-right">
                    <a href="{{ url_for('admin.banner') }}" class="button is-primary is-light mr-2">返回</a>
                    <input type="submit" value="保存" class=" button is-success">
                </div>
            </div>
        </div>
    </form>
{% endblock table_content %}
```

在admin/index.html中增加轮播图url
```text
                    <p class="menu-label">
                        用户管理
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if 'user' in request.path %}is-active{% endif %}"
                                href="{{ url_for('admin.user') }}">用户管理</a>
                        </li>
                    </ul>
                    <p class="menu-label">
                        <span class="icon"><i class="mdi mdi-cog-outline"></i></span>
                        设置
                    </p>
                    <ul class="menu-list">
                        <li><a class="{% if 'banner' in request.path %}is-active{% endif %}"
                            href="{{ url_for('admin.banner') }}">
                            <span class="icon"><i class="mdi mdi-image-sync-outline"></i></span>
                            轮播图管理
                        </a>
                    </li>
                    </ul>
                </aside>
                {% endblock menus %}
```
最后修改base.html中的vue信息
```text
    <script>
        var app = new Vue({
            el: '#app',
            delimiters: ['{$', '$}'],
            data: {
                file:{},
                carousels:[],
                banners: []
            },
            methods: {}
        })
    </script>
    {% block vue_script %}{% endblock vue_script %}
</body>

</html>
```

在首页显示banner图

blog/templates/index.html
```text
{% extends 'base.html' %}

{% block title %} 我的博客 - FlaskBlog {% endblock title %}

{% block hero %}
<div id="banner" style="display:none ;">
    {{ banners }}
</div>
<template>
    <b-carousel>
        <b-carousel-item v-for="(carousel, i) in banners" :key="i">
            <!-- <section :class="`hero is-medium is-${carousel.color}`">
                <div class="hero-body has-text-centered">
                    <h1 class="title">{$ carousel.text $}</h1>
                </div>
            </section> -->
            <a :href="carousel.url">
                <figure class="image is-3by1">
                    <img :src="carousel.img" alt="">
                </figure>
            </a>
        </b-carousel-item>
    </b-carousel>
</template>
{% endblock hero %}

{% block pagination %}
<nav class="pagination is-small" role="navigation" aria-label="pagination">
    {% if pagination.has_prev %}
    <a href="{{ url_for('admin.article') }}?page={{ pagination.prev_num }}" class="pagination-previous" title="This is the first page">Previous</a>
    {% endif %}
    {% if pagination.has_next %}
    <a href="{{ url_for('admin.article') }}?page={{ pagination.next_num }}" class="pagination-next">Next page</a>
    {% endif %}

    <ul class="pagination-list">
        {% for page in pagination.iter_pages() %}
            {% if page %}
                {% if page != pagination.page %}
                <li>
                    <a href="{{ url_for('admin.article') }}?page={{ page }}" class="pagination-link" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% else %}
                <li>
                    <a class="pagination-link is-current" aria-label="Page 1" aria-current="page">{{ page }}</a>
                </li>
                {% endif %}
            {% else %}
                <span class=pagination-ellipsis>&hellip;</span>
            {% endif %}
        {% endfor %}

    </ul>
</nav>
{% endblock pagination %}

{% block vue_script %}
<script>
    app._data.carousels = [
        { text: 'Slide 1', color: 'primary' },
        { text: 'Slide 2', color: 'info' },
        { text: 'Slide 3', color: 'success' },
        { text: 'Slide 4', color: 'warning' },
        { text: 'Slide 5', color: 'danger' }
    ]

    app._data.banners = JSON.parse(document.querySelector('#banner').innerHTML)
    // console.log(app._data.banners)
</script>
{% endblock vue_script %}
```
在blog/templates/views.py中增加banner的返回值
```text
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(
        page=page, per_page=9, error_out=False)
    post_list = pagination.items

    import random
    imgs = [
        'https://scpic.chinaz.net/files/pic/pic7/xpic365.jpg', 
        'https://scpic.chinaz.net/files/pic/pic6/pic1874.jpg', 
        'https://scpic.chinaz.net/files/pic/pic9/201808/zzpic13908.jpg']

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]

    import json
    from app.admin.models import Banner
    banners = Banner.query.all()
    banners_list = [{'img': f'/admin/static/{banner.img}', 'url': banner.url} for banner in banners]
    banners_json = json.dumps(banners_list, ensure_ascii=False)
    return render_template('index.html', posts=post_list, pagination=pagination, banners=banners_json)
```

## 分类和文章之间的级联删除
路径：blog/models.py 修改Category和 Post
```text
class Category(BaseModel):

    """分类模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)

    # post = db.relationship('Post', backref='category', lazy=True)
    post = db.relationship('Post', back_populates="category", cascade="all, delete", passive_deletes=True,)

    def __repr__(self):
        return '<Category %r>' % self.name
        
        
  
class Post(BaseModel):
    """ 文章
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False) 
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    # 多对多关系
    tags = db.relationship('Tag', secondary=tags, 
        lazy='subquery', backref=db.backref('post', lazy=True))
    category = db.relationship("Category", back_populates="post")

    def __repr__(self):
        return '<Post %r>' % self.title
```
修改admin视图中的category_del函数
路径：admin/views.py
```text
@bp.route('/category/delete/<int:cate_id>')
@login_required
def category_del(cate_id):
    cate = Category.query.get(cate_id)
    if cate:
        # 级联删除
        Post.query.filter(Post.category_id == cate.id).delete()
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}分类删除成功')
        return redirect(url_for('admin.category'))
```

## admin管理页面 用户数和文章数按照实际展示
路径： admin/views.py
```text
@bp.route('/')
@login_required
def index():
    # 主页视图
    post_count = Post.query.count()
    user_count = User.query.count()
    return render_template('admin/index.html', post_count=post_count, user_count=user_count)
```

修改页面
路径： admin/templates/admin/index.html
```text
        <div class="tile is-ancestor">
            <div class="tile is-parent">
                <article class="tile is-child notification is-info is-light">
                    <div class="content">
                        <p class="title">{{ post_count }}</p>
                        <p class="subtitle">文章数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
            <div class="tile is-parent">
                <article class="tile is-child notification is-success is-light">
                    <div class="content">
                        <p class="title">{{ user_count }}</p>
                        <p class="subtitle">用户数</p>
                        <div class="content">
                            <!-- Content -->
                        </div>
                    </div>
                </article>
            </div>
```











# 开发过程中遇到的问题
## sqlalchemy.exc.OperationalError: (MySQLdb.OperationalError)
```text
完整错误信息：
sqlalchemy.exc.OperationalError: (MySQLdb.OperationalError) (1130, "Host '10.0.0.1' is not allowed to connect to this MySQL server")

错误原因：
数据库中没有开通远程连接权限

解决方法：
docker exec -it  mysql bash
mysql -uroot -p123456
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
## Flask 表单form.validate_on_submit()总是false
```text
错误信息：
没有明显的错误信息

错误原因：
html中表单的地方没写{{ form.csrf_token }}

解决方法：
在HTML <form></form>里加上{{ form.csrf_token }}就好

```
## jinja2.exceptions.UndefinedError: 'form' is undefined
```text
错误信息：
jinja2.exceptions.UndefinedError: 'form' is undefined

错误原因：
我认为是login.html中引入base.html {% extends 'base.html' %}，但base.html中不存在form.username导致的
实际是：
视图函数auth.py中有也要将from传递给前端：return render_template('login.html', form=form)

解决方法：
视图函数auth.py中有也要将from传递给前端：return render_template('login.html', form=form)
```

## sqlalchemy.exc.IntegrityError
```text
错误信息：
sqlalchemy.exc.IntegrityError: (MySQLdb.IntegrityError) (1062, "Duplicate entry 'guest' for key 'username'")
[SQL: INSERT INTO user (add_date, pub_date, username, password, avatar, is_super_user, is_active, is_staff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)]
[parameters: (datetime.datetime(2022, 11, 14, 15, 17, 27, 504788), datetime.datetime(2022, 11, 14, 15, 17, 27, 504788), 'guest', 'pbkdf2:sha256:260000$Sgn0cpvmWNMx015o$aef1506e758f19b0bbc23f6570871cf126a1964ae4229882c5435a6847d67bce', None, 0, 1, 0)]
(Background on this error at: https://sqlalche.me/e/14/gkpj)

错误原因：
重复注册相同name的用户，就会出现此问题；第一次注册name的用户是可以的。


解决方法：
没能够复现，没有找到解决方法，暂时搁置
```

## RuntimeError: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.
```text
错误信息：
RuntimeError: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.

错误原因：
在工厂函数中没有找到配置文件路径导致。

解决方法：
    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
```

## TypeError: paginate() takes 1 positional argument but 2 positional arguments 
```text
错误信息：
TypeError: paginate() takes 1 positional argument but 2 positional arguments (and 2 keyword-only arguments) were given

错误原因：
参数应该一一对应：pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=9, error_out=False)
通过源码得知：
    def paginate(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = None,
        error_out: bool = True,
        count: bool = True,
    ) -> Pagination:
解决方法：
pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=9, error_out=False)
改为
pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=9, error_out=False)

```
## 功能上的错误
```text
错误信息：
    使用froms表单验证后，注册试图password和password1两次输入不一致，并不会给出error提示。

错误原因：

解决办法：

```

## 添加用户时不选择图片报错
```text
错误信息：
    AttributeError: 'NoneType' object has no attribute 'filename'

错误原因：

解决办法：

```

## 级联删除时当文章带有tag时，删除分类时会报错
```text
错误信息：
    sqlalchemy.exc.IntegrityError: (MySQLdb.IntegrityError) (1451, 'Cannot delete or update a parent row: a foreign key constraint fails (`flaskdb`.`tags`, CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`))')
[SQL: DELETE FROM category WHERE category.id = %s]
[parameters: (3,)]
(Background on this error at: https://sqlalche.me/e/14/gkpj)

Traceback (most recent call last)

错误原因：
    
解决办法：

```

# 在源码的基础上增加功能

```text
1、删除分类时，不要删除分类下的文章
2、代码样式改为带有mac方式的代码框
3、增加笔记功能
4、更换博客主题皮肤
```