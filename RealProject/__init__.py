import os
from RealProject.settings import BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 这操作数据库
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # 这里做了判断是否运行时传入了测试配置
    if test_config is None:
        # 如果没有传入，则从py文件加载配置，silent=True代表文件，文件加载成功则返回True
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置意思一致
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
   
    # 引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    from app.auth import views as auth
    app.register_blueprint(auth.bp)
    from app.admin import views as admin
    app.register_blueprint(admin.bp)

    # url引入
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    # 注册数据库模型
    from app.blog import models
    from app.auth import models
    from app.admin import models

    # 引入上下文
    app.context_processor(inject_category)

    # 注册自定义命令
    from app.admin.utils import init_script
    init_script(app)
    return app


def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。
    上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)