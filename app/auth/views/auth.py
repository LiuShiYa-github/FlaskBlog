import functools
from flask import render_template, Blueprint, redirect, url_for, request, session, flash, g
from ..models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录视图
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = auth.User.query.filter_by(username=username).first()
        if user is None:
            error = '该用户不存在！'
        elif not check_password_hash(user.password, password):
            error = '密码不正确.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册视图
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        user = auth.User.query.filter_by(username=username).first()

        if password != password1:
            flash('两次密码输入不一致！')
            return redirect(url_for('auth.register'))

        # exists_user = auth.User.query.filter_by(username=username).first()
        if user:
            flash('该用户名已经存在，请更换其他用户名！')
            # return redirect(url_for('auth.register'))
        else:
            # 添加一个用户信息到数据库
            u = auth.User(username=username, password=generate_password_hash(password1))
            db.session.add(u)
            db.session.commit()

            # 自动登录效果
            session.clear()
            session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('register.html')


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect(url_for('index'))


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
