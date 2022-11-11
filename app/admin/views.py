from ctypes import pointer
from flask import (
    Blueprint, render_template, request, 
    flash, redirect, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from app.auth.views.auth import login_required
from app.blog.models import Category, Post, Tag
from app.auth.models import User
from .models import Banner
from .forms import CategoryForm, PostForm, TagForm, CreateUserForm


bp = Blueprint('admin', __name__, url_prefix='/admin', 
    static_folder='static', template_folder='templates')


@bp.route('/')
@login_required
def index():
    post_count = Post.query.count()
    user_count = User.query.count()
    return render_template(
        'admin/index.html', post_count=post_count, user_count=user_count)


@bp.route('/category')
@login_required
def category():
    # 查看分类
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(
        -Category.add_date).paginate(
            page, per_page=10, error_out=False)
    category_list = pagination.items
    return render_template(
        'admin/category.html', 
        category_list=category_list, 
        pagination=pagination
    )


@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    # 新增博客分类
    form = CategoryForm()
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
    # 编辑博客分类
    cate = Category.query.get(cate_id)
    form = CategoryForm(name=cate.name, icon=cate.icon)
    if form.validate_on_submit():
        cate.name = form.name.data
        cate.icon = form.icon.data
        db.session.add(cate)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)


@bp.route('/category/delete/<int:cate_id>')
@login_required
def category_del(cate_id):
    cate = Category.query.get(cate_id)
    if cate:
        # 级联删除
        Post.query.filter(Post.category_id==cate.id).delete()
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}分类删除成功')
        return redirect(url_for('admin.category'))


@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(
        page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template(
        'admin/article.html', 
        post_list=post_list, 
        pagination=pagination
    )


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 新增博客分类
    form = PostForm()   
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            desc=form.desc.data,
            has_type=form.has_type.data,
            category_id=int(form.category_id.data),  # 一对多保存
            content=form.content.data
        )
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data ]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}添加成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)


@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    
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
        # 这里才是修改的逻辑
        print(type(form.has_type.data))
        # 一个,引起的bug  StatementError
        post.title=form.title.data
        post.desc=form.desc.data
        post.has_type=form.has_type.data
        post.category_id=int(form.category_id.data)  # 一对多保存
        post.content=form.content.data
        post.tags=[Tag.query.get(tag_id) for tag_id in form.tags.data ]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form, post=post)


@bp.route('/article/delete/<int:post_id>')
@login_required
def article_del(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}删除成功')
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
        flash(f'{form.name.data}修改成功')
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
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(-User.add_date).paginate(
        page, per_page=10, error_out=False)
    user_list = pagination.items
    return render_template(
        'admin/user.html', 
        user_list=user_list, 
        pagination=pagination)


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
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


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    # 修改用户信息
    user = User.query.get(user_id)
    form = CreateUserForm(
        username=user.username,
        password=user.password,
        avatar=user.avatar,
        is_super_user=user.is_super_user,
        is_active=user.is_active,
        is_staff=user.is_staff 
    )
    if form.validate_on_submit():
        user.username = form.username.data
        if not form.password.data:
            user.password = user.password
        else:
            user.password = generate_password_hash(form.password.data)

        from .utils import upload_file_path
        f = form.avatar.data
        print(form.avatar.data)
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
        flash(f'{user.username}修改成功！')
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
        # 获取一个文件类型 request.files
        f = request.files.get('upload')
        file_size = len(f.read())
        f.seek(0)  # reset cursor position to beginning of file

        if file_size > 2048000:  # 限制上传大小为2M
            return {
                'code':'err',
                'message': '文件超过限制2048000字节',
            }
        
        from .utils import upload_file_path
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {
            'code':'ok',
            'url':f'/admin/static/upload/{filename}'
        }


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

