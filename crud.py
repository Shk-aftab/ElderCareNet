from sqlalchemy.orm import Session
import bcrypt
from models import User, Article, Comment, SavedArticle, Admin
import schemas

# ----- User CRUD -----
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = User(name=user.name, email=user.email, age=user.age, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

# ----- Article CRUD -----
def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.article_id == article_id).first()

def create_article(db: Session, article: schemas.ArticleCreate, author_id: int):
    db_article = Article(title=article.title, content=article.content, author_id=author_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: int, article_update: schemas.ArticleCreate):
    article = db.query(Article).filter(Article.article_id == article_id).first()
    if article:
        article.title = article_update.title
        article.content = article_update.content
        db.commit()
        db.refresh(article)
    return article

def delete_article(db: Session, article_id: int):
    article = db.query(Article).filter(Article.article_id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
    return article

# ----- Comment CRUD -----
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = Comment(content=comment.content, article_id=comment.article_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_article(db: Session, article_id: int):
    return db.query(Comment).filter(Comment.article_id == article_id).all()

# ----- Saved Article CRUD -----
def save_article(db: Session, user_id: int, saved_article: schemas.SavedArticleCreate):
    db_saved = SavedArticle(user_id=user_id, article_id=saved_article.article_id)
    db.add(db_saved)
    db.commit()
    db.refresh(db_saved)
    return db_saved

def get_saved_articles(db: Session, user_id: int):
    return db.query(SavedArticle).filter(SavedArticle.user_id == user_id).all()

# ----- Admin CRUD -----
def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()

def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_password = bcrypt.hashpw(admin.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_admin = Admin(name=admin.name, email=admin.email, password_hash=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin
