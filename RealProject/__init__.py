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
    from app.blog.views import blog as blog
    from app.auth.views import auth as auth
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    # url引入
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    # 注册数据库模型
    from app.blog.models import blog
    from app.auth.models import auth

    return app
