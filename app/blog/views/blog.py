from flask import Blueprint, render_template

bp = Blueprint('blog', __name__, url_prefix='/blog', static_folder='../static', template_folder='../templates')


def index():
    """首页视图
    """
    posts = [1, 2, 3, 4, 5, 6]
    return render_template('index.html', posts=posts)
