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
from app.blog.models import Category, Post, Tag


def index():
    """ 首页视图 """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page, per_page=9, error_out=False)
    post_list = pagination.items

    import random
    imgs = [
        'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.jj20.com%2Fup%2Fallimg%2Ftp01%2F1ZZH250054149-0-lp.jpg&refer=http%3A%2F%2Fimg.jj20.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1665669152&t=45ceedb22949717bfd414f17a36d6752',
        'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fimg.jj20.com%2Fup%2Fallimg%2Ftp09%2F21031FKU44S6-0-lp.jpg&refer=http%3A%2F%2Fimg.jj20.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1665669130&t=bae679c92a2833ac185cb5ef8f834aae',
        'https://img2.baidu.com/it/u=1853461411,445981998&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500']

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
        # post.img = random.choice(imgs)

    return render_template('index.html', posts=post_list, pagination=pagination)


@bp.route('/hello')
def hello():
    return 'Hello, World!'


@bp.route('/flask')
def helloflask():
    return 'Hello, Flask!'


@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    # 分类页
    cate = Category.query.get(cate_id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.category_id == cate_id).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('cate_list.html', cate=cate, post_list=post_list, cate_id=cate_id, pagination=pagination)


@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id, post_id):
    # 详情页
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)
    # print("我在这里：{}".format(post.tags))

    # 上一篇
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    # 下一篇
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    return render_template('detail.html', cate=cate, post=post, prev_post=prev_post, next_post=next_post)


@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])

    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info',
                     'is-warning']

    # 最新文章
    new_posts = posts.limit(6)
    return dict(dates=dates, tags=tags, new_posts=new_posts)


@bp.route('/category/<string:date>')
def archive(date):
    # 归档页
    import re
    # 正则匹配年月
    regex = re.compile(r"\d{4}|\d{2}")
    dates = regex.findall(date)

    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    # 根据年月获取数据
    archive_posts = Post.query.filter(
        and_(extract('year', Post.add_date) == int(dates[0]), extract('month', Post.add_date) == int(dates[1])))
    # 对数据进行分页
    pagination = archive_posts.paginate(page, per_page=10, error_out=False)
    return render_template('archive.html', post_list=pagination.items, pagination=pagination, date=date)


@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    # 标签页
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)


@bp.route('/search')
def search():
    # 搜索视图
    words = request.args.get('words', '', type=str)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.title.like("%"+words+"%")).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('search.html', post_list=post_list, words=words, pagination=pagination)
