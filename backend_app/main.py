from datetime import timedelta, date

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from typing import Annotated

from backend_app import models, crud, schemas, database, security
from backend_app.database import SessionLocal, engine

from backend_app.services import generate_plots, find_items

from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()


def execute_job():
    subprocess.run(["/bin/sh", "cron_jobs/job.sh"])


@scheduler.scheduled_job("cron", hour=17)
def run_job():
    execute_job()

app.mount("/static", StaticFiles(directory="backend_app/static"), name="static")

templates = Jinja2Templates(directory="backend_app/templates")


@app.get("/")
async def home(request: Request, db: Session = Depends(database.get_db)):
    # TODO make product globall variable (performance)
    products = find_items(db)
    return templates.TemplateResponse('main.html', {'request': request, 'products': products})


@app.get("/generate_plots/")
def graph_create(current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
                 db: Session = Depends(database.get_db)):
    # TODO check if current user have admin role else raise error
    generate_plots(db)
    return {"status": "success"}


@app.post("/add_entries/", response_model=schemas.Price)
async def create_entry(entry: schemas.PriceEntry, db: Session = Depends(database.get_db)):
    db_item = crud.get_item_by_id(db=db, id=entry.item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="The item does not exist")
    return crud.add_item_price(db=db, price_entry=entry)


@app.post("/auth/signup/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/auth/signin/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.get_db)
):
    user = security.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    subscription = crud.get_last_subscription_by_user_id(db, user_id=user.id)

    if subscription.end_date < date.today():
        crud.update_user_subscribed_false(db, id=user.id)
        return {"access_token": access_token, "token_type": "bearer", "is_subscribed": False, "end_date": None }
    else:
        return {"access_token": access_token, "token_type": "bearer", "is_subscribed": True, "end_date": subscription.end_date.strftime("%d/%m/%Y")}

    


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(
        security.get_current_active_user)]
):
    return current_user


@app.post("/comment/", response_model=schemas.Comment)
async def create_comment(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    comment_form: schemas.CommentForm,
    db: Session = Depends(database.get_db)
):
    db_item = crud.get_item_by_id(db=db, id=comment_form.item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="The item does not exist")
    comment = schemas.CommentCreate(text=comment_form.text,
                                    user_id=current_user.id,
                                    item_id=comment_form.item_id)
    return crud.add_coment_to_item(db=db, comment=comment)


@app.delete("/comment/{comment_id}/")
async def delete_comment(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    comment_id: int,
    db: Session = Depends(database.get_db)
):
    deleted_comment = crud.delete_comment(
        db=db, comment_id=comment_id, user_id=current_user.id)

    if not deleted_comment:
        raise HTTPException(
            status_code=404, detail="Comment not found or user does not have access"
        )

    return deleted_comment


@app.post("/follow/", response_model=schemas.ItemFollowers)
async def follow_item(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    follow_request: schemas.FollowRequest,
    db: Session = Depends(database.get_db)
):
    db_item = crud.get_item_by_id(db=db, id=follow_request.item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="The item does not exist")
    follow_item = crud.add_item_to_item_followers(
        db=db, user_id=current_user.id, item_id=follow_request.item_id)
    if not follow_item:
        raise HTTPException(
            status_code=400, detail="The user is already following this item")
    return follow_item


@app.post("/unfollow/", response_model=schemas.ItemFollowers)
async def follow_item(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    follow_request: schemas.FollowRequest,
    db: Session = Depends(database.get_db)
):
    db_item = crud.get_item_by_id(db=db, id=follow_request.item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="The item does not exist")
    follow_item = crud.remove_item_from_item_followers(
        db=db, user_id=current_user.id, item_id=follow_request.item_id)
    if not follow_item:
        raise HTTPException(
            status_code=400, detail="The user is not following this item")
    return follow_item


@app.get("/items/")
async def get_items(current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
                    db: Session = Depends(database.get_db)):
    products = crud.get_items_with_comments(db)
    return products


@app.get("/item_prices/")
async def get_item_prices(current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
                          item_id: int,
                          db: Session = Depends(database.get_db)
                          ):

    item = crud.get_item_by_id(db, item_id)
    return item.prices


@app.get("/followed_items/")
async def get_followed_items(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    db: Session = Depends(database.get_db)
):
    followed_items = crud.get_items_followed_by_user(db, current_user.id)
    return [{"id": item.item.id, "name": item.item.name} for item in followed_items]

