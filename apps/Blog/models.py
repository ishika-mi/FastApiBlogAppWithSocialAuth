from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, String, Column, DateTime, Integer, Boolean, Text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import relationship

from apps.database import Base
from apps.Users.models import User


class Blog(Base):
    __tablename__ = 'blog'

    blog_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    author_id =  Column(Integer,ForeignKey("users.user_id"))
    author = relationship("User",back_populates="blogs")
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.title = kwargs.get("title")
        self.content = kwargs.get("content")
        self.author_id = kwargs.get("author_id")

    @classmethod
    def save(cls, db_session, data):
        try:
            blog = cls(**data)
            db_session.add(blog)
            db_session.commit()
            db_session.refresh(blog)
            return True, blog
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    @classmethod
    def get_user_by_id(cls, db_session: Any, blog_id: int):
        return db_session.query(cls).filter(cls.blog_id == blog_id).first()

    @classmethod
    def get_user_by_title(cls, db_session: Any, title: str):
        return db_session.query(cls).filter(cls.title == title).first()

    @classmethod
    def get_user_by_author_id(cls, db_session: Any, author_id: int):
        return db_session.query(cls).filter(cls.author_id == author_id).first()

    def __repr__(self) -> str:
        return f"<User {self.blog_id}>"
