from datetime import datetime
from RealProject import db
from enum import IntEnum
from sqlalchemy.dialects.mysql import LONGTEXT


class BaseModel(db.Model):
    # 基类模型
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow, nullable=False)  # 更新时间


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


class Category(BaseModel):
    """分类模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)

    # post = db.relationship('Post', backref='category', lazy=True)
    post = db.relationship('Post', back_populates="category", cascade="all, delete", passive_deletes=True, )

    def __repr__(self):
        return '<Category %r>' % self.name


# 多对多关系帮助器表
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                )


class Post(BaseModel):
    """ 文章
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    # 多对多关系
    tags = db.relationship('Tag', secondary=tags,
                           lazy='subquery', backref=db.backref('post', lazy=True))
    category = db.relationship("Category", back_populates="post")

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(BaseModel):
    """ 文章标签
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return self.name
