from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import timedelta

import schemas
import crud
import auth
from auth import get_db, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_admin, get_current_admin

router = APIRouter()

from template_config import admin_templates

# New admin root endpoint to serve the login page
@router.get("/")
async def admin_root(request: Request):
    return admin_templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/token")
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": admin.email}, expires_delta=access_token_expires)
    response = RedirectResponse(url="/admin/dashboard", status_code=302)
    response.set_cookie("access_token", access_token)
    return response

@router.get("/dashboard")
async def admin_dashboard(request: Request, db: Session = Depends(get_db), current_admin: schemas.AdminOut = Depends(get_current_admin)):
    articles = crud.get_articles(db)
    return admin_templates.TemplateResponse("admin_dashboard.html", {"request": request, "admin": current_admin, "articles": articles})

@router.get("/article/create")
async def create_article_form(request: Request):
    return admin_templates.TemplateResponse("create_article.html", {"request": request})

@router.post("/article/create")
async def create_article(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: schemas.AdminOut = Depends(get_current_admin)
):
    article_data = schemas.ArticleCreate(title=title, content=content)
    crud.create_article(db, article_data, current_admin.admin_id)
    return RedirectResponse(url="/admin/dashboard", status_code=302)

@router.get("/article/{article_id}/edit")
async def edit_article_form(article_id: int, request: Request, db: Session = Depends(get_db), current_admin: schemas.AdminOut = Depends(get_current_admin)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return admin_templates.TemplateResponse("edit_article.html", {"request": request, "article": article})

@router.post("/article/{article_id}/edit")
async def edit_article(
    article_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: schemas.AdminOut = Depends(get_current_admin)
):
    article_data = schemas.ArticleCreate(title=title, content=content)
    crud.update_article(db, article_id, article_data)
    return RedirectResponse(url="/admin/dashboard", status_code=302)

@router.post("/article/{article_id}/delete")
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_admin: schemas.AdminOut = Depends(get_current_admin)
):
    crud.delete_article(db, article_id)
    return RedirectResponse(url="/admin/dashboard", status_code=302)
