from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from backend_app import models, crud, schemas
from backend_app.database import SessionLocal, engine

from backend_app.services import generate_plots, find_items

from fastapi.middleware.cors import CORSMiddleware

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="backend_app/static"), name="static")

templates = Jinja2Templates(directory="backend_app/templates")

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    products = find_items(db)
    return templates.TemplateResponse('main.html', {'request': request, 'products': products})

@app.get("/generate_plots")
def graph_create(db: Session = Depends(get_db)):
    generate_plots(db)
    return {"status": "success"}

@app.post("/add_entries", response_model=schemas.Item)
async def create_entry(entry: schemas.ItemEntry, db: Session = Depends(get_db)):
    return crud.add_item_entry(db=db, entry=entry)