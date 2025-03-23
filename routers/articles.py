from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import schemas
import crud
import auth
from auth import get_db, get_current_user

router = APIRouter()

from template_config import user_templates


@router.get("/")
async def list_articles(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_articles(db)
    return user_templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@router.get("/{article_id}")
async def read_article(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    comments = crud.get_comments_by_article(db, article_id)
    return user_templates.TemplateResponse("article.html", {"request": request, "article": article, "comments": comments})

@router.post("/{article_id}/comment")
async def post_comment(
    article_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    comment_data = schemas.CommentCreate(content=content, article_id=article_id)
    crud.create_comment(db, comment_data, current_user.user_id)
    return RedirectResponse(url=f"/articles/{article_id}", status_code=302)

@router.post("/{article_id}/save")
async def save_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    saved_data = schemas.SavedArticleCreate(article_id=article_id)
    crud.save_article(db, current_user.user_id, saved_data)
    return RedirectResponse(url="/users/dashboard", status_code=302)

@router.get("/saved")
async def saved_articles(request: Request, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    saved = crud.get_saved_articles(db, current_user.user_id)
    articles = [crud.get_article(db, s.article_id) for s in saved]
    return user_templates.TemplateResponse("saved.html", {"request": request, "articles": articles})
