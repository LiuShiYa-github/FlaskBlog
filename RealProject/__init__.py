#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: __init__.py.py
@Time    : 2022/8/14 18:25
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 官方说明：https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from RealProject.settings import BASE_DIR
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # 绑定数据库
    db.init_app(app)
    # 注册migrate
    migrate.init_app(app, db)

    # ensure the instance folder exists
    # 这里好像是可以注释的
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # 注册blog.
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    # 注册auth
    from app.auth.views import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    # 注册admin
    from app.admin import views as admin
    app.register_blueprint(admin.bp)
    app.add_url_rule(rule='/', endpoint='index', view_func=blog.index)

    # 注册数据库模型, 这里pychrom提示说import的包没有被引用，忽略此提示就好，注释的话会导致数据库没有创建表
    from app.blog import models
    from app.auth.models import auth

    # 全局上下文
    app.context_processor(inject_category)

    return app


def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)
