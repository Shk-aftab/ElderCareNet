from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    font_size_preference: Optional[str]

class UserOut(UserBase):
    user_id: int
    age: Optional[int]
    font_size_preference: str
    created_at: datetime

    class Config:
        orm_mode = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleOut(ArticleBase):
    article_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    author_id: int

    class Config:
        orm_mode = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    article_id: int

class CommentOut(CommentBase):
    comment_id: int
    article_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Saved Article Schemas
class SavedArticleCreate(BaseModel):
    article_id: int

class SavedArticleOut(BaseModel):
    saved_id: int
    user_id: int
    article_id: int
    saved_at: datetime

    class Config:
        orm_mode = True

# Admin Schemas
class AdminBase(BaseModel):
    name: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminOut(AdminBase):
    admin_id: int
    created_at: datetime

    class Config:
        orm_mode = True
