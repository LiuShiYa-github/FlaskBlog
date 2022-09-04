#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: auth.py
@Time    : 2022/8/16 19:32
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 
"""
import functools
from ..forms import LoginForm, RegisterForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from ..models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect(url_for('auth.login'))


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
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


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
            redirect_to = f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
        return view(**kwargs)
    return wrapped_view
