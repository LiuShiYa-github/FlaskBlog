import functools
from ..forms import LoginForm, RegisterForm
from flask import render_template, Blueprint, redirect, url_for, request, session, flash, g
from app.auth.models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db

from app.auth.models.auth import User

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')


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


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect('/')


@bp.route('/')
@login_required
def userinfo():
    # 用户中心
    return render_template('userinfo.html')
