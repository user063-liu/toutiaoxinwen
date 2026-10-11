from datetime import datetime
from tokenize import String
from typing import Optional

from pygments.lexer import default
from sqlalchemy import func, DateTime, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="更新时间")


class Category(Base):
    __tablename__ = "news_category"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True, comment="id")
    name : Mapped[str] = mapped_column(String(50), comment="名字", unique=True)
    sort_order : Mapped[int] = mapped_column(Integer, comment="描述", unique=True)


    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"



class News(Base):
    __tablename__ = "news"


    __table_args__ = (
        Index('fk_news_category_id', 'category_id'),  #  高频查询
        Index('idx_publish_time', 'publish_time')  # 按发布时间查询
    )

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻Id")
    title : Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description : Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content : Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image : Mapped[Optional[str]] = mapped_column(String(255), comment="封面照片URL")
    author : Mapped[Optional[str]] = mapped_column((String(50)), comment="作者")
    category_id : Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"),nullable=False, comment="分类Id")
    views : Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")


    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
