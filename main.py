from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse

from routers import users, articles, admin
import auth
import crud
import schemas

from template_config import common_templates, user_templates, admin_templates


app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")



# Include routers for different endpoints
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# New root route that shows the landing page
@app.get("/")
async def landing(request: Request):
    return user_templates.TemplateResponse("landing.html", {"request": request})

@app.get("/logout")
async def logout(response: Response):
    # Clear the access token cookie
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

# Dummy data seeding route (for development/testing only)
@app.get("/seed")
async def seed_data(request: Request, db: Session = Depends(auth.get_db)):
    # Create dummy user if not exists
    user = crud.get_user_by_email(db, "user@example.com")
    if not user:
        dummy_user = schemas.UserCreate(name="John Doe", email="user@example.com", password="password", age=60)
        crud.create_user(db, dummy_user)
    # Create dummy admin if not exists
    admin_user = crud.get_admin_by_email(db, "admin@example.com")
    if not admin_user:
        dummy_admin = schemas.AdminCreate(name="Admin", email="admin@example.com", password="adminpassword")
        crud.create_admin(db, dummy_admin)
    # Create dummy article if none exist
    articles_list = crud.get_articles(db)
    if not articles_list:
        dummy_article = schemas.ArticleCreate(title="Healthy Living Tips", content="Stay active and eat healthy!")
        crud.create_article(db, dummy_article, 1)
    return {"message": "Dummy data seeded"}

