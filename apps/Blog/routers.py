from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.Blog.schemas import CreateBlog, ShowBlog, UpdateBlog
from apps.Blog.services import BlogService
from apps.Users.models import User
from fastapi import status
from apps.database import get_db
from apps.language import Response

from apps.database import get_db
from apps.utils import get_current_active_user_id

blog_api_router = APIRouter(
    tags=["blog"],
    prefix="/blog",
)

@blog_api_router.post("/blog",response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session= Depends(get_db), user_id: int = Depends(get_current_active_user_id)):
    blog = BlogService.create_new_blog(blog=blog,db=db,author_id=user_id)
    return blog

@blog_api_router.get("/blog/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session= Depends(get_db)):
    blog = BlogService.retreive_blog(id=id, db=db)
    if not blog:
        return Response.send_error_response(f"Blog with ID {id} does not exist.",status_code=status.HTTP_404_NOT_FOUND)
    return blog

@blog_api_router.get("/blogs",response_model=List[ShowBlog])
def get_all_blogs(db:Session = Depends(get_db)):
    blogs = BlogService.list_blogs(db=db)
    return blogs

@blog_api_router.put("/blog/{id}",response_model=ShowBlog)
def update_a_blog(id:int,blog:UpdateBlog, db:Session = Depends(get_db), user_id: int = Depends(get_current_active_user_id)):
    blog = BlogService.update_blog(id=id,blog=blog,author_id=user_id,db=db)
    if not blog:
        return Response.send_error_response(f"Blog with ID {id} does not exist.",status_code=status.HTTP_404_NOT_FOUND)
    return blog

@blog_api_router.delete("/delete/{id}")
def delete_a_blog(id:int, db: Session = Depends(get_db),   user_id: int = Depends(get_current_active_user_id)):
    message = BlogService.delete_blog(id=id,author_id=user_id,db=db)
    if message.get("error"):
        return Response.send_error_response(message.get("error"),status_code=status.HTTP_400_BAD_REQUEST)
    return {"msg":f"Successfully deleted blog with id {id}"}