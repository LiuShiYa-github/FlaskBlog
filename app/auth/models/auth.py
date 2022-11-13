from datetime import datetime
from RealProject import db


class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )  # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 更新时间


class User(BaseModel):
    """用户模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(320), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    is_super_user = db.Column(db.Boolean, nullable=True, default=False)  # 超级管理员标识
    is_active = db.Column(db.Boolean, nullable=True, default=True)  # 是否为活跃用户
    is_staff = db.Column(db.Boolean, nullable=True, default=False)  # 是否允许登录后台

    def __repr__(self):
        return '<Category %r>' % self.username
