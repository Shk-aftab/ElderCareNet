from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import schemas
import crud
import auth
from fastapi.security import OAuth2PasswordRequestForm
from auth import get_db, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user
from datetime import timedelta


router = APIRouter()

from template_config import user_templates

MINIMUM_AGE = 50  # Set your minimum age requirement here


# New endpoint to check email existence
@router.post("/check_email")
async def check_email(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user:
        # User exists; redirect to login page with email pre-filled
        return user_templates.TemplateResponse("login.html", {"request": request, "email": email})
    else:
        # User does not exist; redirect to registration page with email pre-filled
        return user_templates.TemplateResponse("register.html", {"request": request, "email": email})

# Registration endpoint accepts form data
@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    db: Session = Depends(get_db)
):
    # Server-side age check
    if age < MINIMUM_AGE:
        raise HTTPException(status_code=400, detail=f"Registration allowed for users aged {MINIMUM_AGE} and above.")
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = schemas.UserCreate(name=name, email=email, password=password, age=age)
    crud.create_user(db, user_data)
    # After successful registration, redirect to the login page with email pre-filled.
    return RedirectResponse(url="/", status_code=302)



@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # Redirecting to the dashboard after successful login
    response = RedirectResponse(url="/users/dashboard", status_code=302)
    response.set_cookie("access_token", access_token)  # Optionally set a cookie
    return response

@router.get("/dashboard")
async def user_dashboard(request: Request, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    articles = crud.get_articles(db)
    return user_templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user, "articles": articles})

@router.get("/profile")
async def get_profile(request: Request, current_user: schemas.UserOut = Depends(auth.get_current_user)):
    return user_templates.TemplateResponse("profile.html", {"request": request, "user": current_user})

@router.post("/profile/update")
async def update_profile(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(None),
    font_size_preference: str = Form(...),
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user)
):
    update_data = schemas.UserUpdate(name=name, email=email, age=age, font_size_preference=font_size_preference)
    crud.update_user(db, current_user.user_id, update_data)
    return RedirectResponse(url="/users/profile", status_code=302)
