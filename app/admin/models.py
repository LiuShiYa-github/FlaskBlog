from datetime import datetime, timedelta
from RealProject import db


class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, ) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # 更新时间


class Banner(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(300), nullable=True)

    def __repr__(self) -> str:
        return f'{self.id}=>{self.img}'