#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: views.py
@Time    : 2022/8/21 14:57
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_sqlalchemy import Pagination
from app.auth.views.auth import login_required
from app.blog.models import Category, Post, Tag
from app.auth.models.auth import User
from app.admin.forms import CategoryCreateForm, PostForm, TagForm, CreateUserForm
from RealProject import db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/category')
@login_required
def category():
    page = request.args.get('page', 1, int)
    pagination = Category.query.order_by(-Category.add_date).paginate(page, per_page=5, error_out=False)
    # print([i for i in pageination.iter_pages()])
    category_list = pagination.items
    return render_template('admin/category.html', category_list=category_list, pagination=pagination)


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


@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('admin/article.html', post_list=post_list, pagination=pagination)


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 增加文章
    form = PostForm()
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]

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


@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(
        title=post.title,
        desc=post.desc,
        category_id=post.category.id,
        has_type=post.has_type.value,
        content=post.content,
        tags=tags
    )

    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id = int(form.category_id.data)
        post.content = form.content.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)


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


@bp.route('/user')
@login_required
def user():
    # 查看用户列表
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(-User.add_date).paginate(page, per_page=10, error_out=False)
    user_list = pagination.items
    return render_template('admin/user.html', user_list=user_list, pagination=pagination)


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    # 添加用户
    # https://flask-wtf.readthedocs.io/en/1.0.x/form/#file-uploads
    from .utils import upload_file_path
    form = CreateUserForm()
    if form.validate_on_submit():
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
        return redirect(url_for('admin.user'))
    return render_template('admin/user_form.html', form=form)


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
                'code': 'err',
                'message': '文件超过限制2048000字节',
            }
        from .utils import upload_file_path
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {
            'code': 'ok',
            'url': f'/admin/static/upload/{filename}'
        }
