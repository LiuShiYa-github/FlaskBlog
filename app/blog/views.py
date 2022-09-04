#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: views.py
@Time    : 2022/8/14 19:29
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


def index():
    """ 首页视图 """
    posts = [1, 2, 3, 4, 5, 6]
    return render_template('index.html', posts=posts)


@bp.route('/hello')
def hello():
    return 'Hello, World!'


@bp.route('/flask')
def helloflask():
    return 'Hello, Flask!'
