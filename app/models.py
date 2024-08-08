from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    posts: Mapped[List['Post']] = relationship(back_populates='owner')


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(server_default='true')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    owner_id = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped[User] = relationship(back_populates='posts')

    
class Vote(Base):
    __tablename__ = "votes"
    
    post_id = mapped_column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())