from sqlalchemy.orm import Session 
from fastapi import status
from apps.Blog.models import Blog
from apps.Users.models import User
from apps.language import Response



from apps.Blog.schemas import CreateBlog, UpdateBlog

class BlogService:
    @staticmethod
    def create_new_blog(blog: CreateBlog, db: Session, author_id: int):
        blog_data = blog.model_dump()
        blog = Blog(**blog_data, author_id=author_id,author = User.get_user_by_id(user_id=author_id,db_session=db))
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog
    @staticmethod
    def retreive_blog(id: int, db: Session):
        blog = db.query(Blog).filter(Blog.blog_id == id).first()
        return blog
    @staticmethod
    def list_blogs(db:Session):
        blogs = db.query(Blog).filter(Blog.is_active==True).all()
        return blogs
    
    @staticmethod
    def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
        blog_in_db = db.query(Blog).filter(Blog.blog_id == id).first()
        if not blog_in_db:
            return Response.send_error_response("Blog with id {id} does not exist",status_code = status.HTTP_404_NOT_FOUND)
        if not blog_in_db.author_id == author_id:
            return Response.send_error_response(f"Only the author can modify the blog",status_code=status.HTTP_401_UNAUTHORIZED)
        blog_in_db.title = blog.title
        blog_in_db.content = blog.content
        db.add(blog_in_db)
        db.commit()
        return blog_in_db

    @staticmethod
    def delete_blog(id: int, author_id: int, db: Session):
        blog_in_db = db.query(Blog).filter(Blog.blog_id == id)
        if not blog_in_db.first():
            return Response.send_error_response("Blog with id {id} does not exist",status_code = status.HTTP_404_NOT_FOUND)
        if not blog_in_db.first().author_id ==author_id:
            return Response.send_error_response(f"Only the author can delete the blog",status_code=status.HTTP_401_UNAUTHORIZED)
        blog_in_db.delete()
        db.commit()
        return {"msg": f"deleted blog with id {id}"}