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
import json
import secrets

from authlib.integrations.starlette_client import OAuth, OAuthError

from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('backend_app/.env')
print(config.__dict__)
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=str(CONF_URL),
    client_kwargs={
        'scope': 'openid email profile'
    }
)

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

frontend_url = "http://localhost:5173"

@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/auth/google_signin/">login</a>')


@app.get('/auth/google_signin/')
async def login_user_via_google(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/google_auth/"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth/google_auth/')
async def auth(request: Request, db: Session = Depends(database.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return error
    user = token.get('userinfo')

    db_user = crud.get_user_by_email(db, email=user['email'])

    if not db_user:
        google_user = schemas.UserCreate(
            username=user['name'], email=user['email'], password=secrets.token_hex(16))
        db_user = crud.create_user(db=db, user=google_user)

    subscription = crud.get_last_subscription_by_user_id(db, user_id=db_user.id)

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    if user:
        request.session['user'] = dict(user)

    redirect_url = f"{frontend_url}/?access_token={access_token}&is_subscribed={subscription is not None}"
    if subscription is not None:
        redirect_url += f"&end_date={subscription.end_date.strftime('%d/%m/%Y')}"
    
    return RedirectResponse(url=redirect_url)

@app.get('/logout/')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


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


@app.post("/auth/signup/", response_model=schemas.SignupResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return schemas.SignupResponse(
        user=crud.create_user(db=db, user=user),
        token=security.create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
)

@app.post("/auth/signin/", response_model=schemas.Token)
async def login_for_access_token(
    user: schemas.UserLogin,
    db: Session = Depends(database.get_db)
):
    user = security.authenticate_user(
        db=db, username=user.username, password=user.password)
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
    if subscription == None:
        return {"access_token": access_token, "token_type": "bearer", "is_subscribed": False, "end_date": None}
    else:
        if subscription.end_date < date.today():
            crud.update_user_subscribed_false(db, id=user.id)
            return {"access_token": access_token, "token_type": "bearer", "is_subscribed": False, "end_date": None}
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
    items = crud.get_items(db)
    items_dto = [map_to_item_dto(item=item, db=db) for item in items]
    return items_dto


@app.get("/item_prices/")
async def get_item_prices(item_id: int, db: Session = Depends(database.get_db)):
    item = crud.get_item_by_id(db, item_id)
    return item.prices


@app.get("/newest_item_price/")
async def get_item_newest_price_by_item_id(item_id: int, db: Session = Depends(database.get_db)):
    newset_price = crud.get_newest_price(db=db, item_id=item_id) 
    if not newset_price:
        raise HTTPException(
            status_code=400, detail="Newest price not found.")
    return newset_price

@app.get("/followed_items/")
async def get_followed_items(
    current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
    db: Session = Depends(database.get_db)
):
    followed_items = crud.get_items_followed_by_user(db, current_user.id)
    items: models.Item = map(lambda followed_item: followed_item.item, followed_items)
    items_dto = [map_to_item_dto(item=item, db=db) for item in items]
    return items_dto


@app.get("/user_subscription/")
async def get_user_subscription(
        current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
        db: Session = Depends(database.get_db)):
    user_subscription = crud.get_last_subscription_by_user_id(
        db, current_user.id)
    if user_subscription:
        if user_subscription.end_date > date.today():
            return user_subscription
    return None


@app.get("/all_user_subscriptions/")
async def get_user_subscription(
        current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
        db: Session = Depends(database.get_db)):
    user_subscriptions = crud.get_all_subscriptions_by_user_id(
        db, current_user.id)
    if user_subscriptions:
        return user_subscriptions
    return None


@app.post("/create_user_subscription/")
async def create_user_subscription(
        current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
        sub_request: schemas.SubscriptionRequest,
        db: Session = Depends(database.get_db)):
    last_subscription = crud.get_last_subscription_by_user_id(
        db, current_user.id)
    if last_subscription:
        if last_subscription.end_date > date.today():
            return HTTPException(status_code=400, detail="User already has an active subscription")
    months = sub_request.months
    start_date = date.today()
    end_date = start_date + timedelta(days=(months*30))
    user_subscription = crud.add_subscription(
        db, start_date, end_date, current_user.id)
    if not user_subscription:
        return HTTPException(status_code=400, detail="Error creating subscription")
    return user_subscription


@app.post("/delete_current_user_subscription/")
async def create_user_subscription(
        current_user: Annotated[schemas.User, Depends(security.get_current_active_user)],
        db: Session = Depends(database.get_db)):
    return crud.delete_current_subscription(db, current_user.id)


def map_to_item_dto(item: models.Item, db: Session):
    return {
        "id": item.id,
        "name": item.name,
        "item_img_url": item.item_img_url,
        "newest_price": crud.get_newest_price(db=db, item_id=item.id)
    }