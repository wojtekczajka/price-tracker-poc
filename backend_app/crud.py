from sqlalchemy.orm import Session

from backend_app import models, schemas, security


def get_item_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemEntry).offset(skip).limit(limit).all()


def add_item_entry(db: Session, entry: schemas.ItemEntry):
    item_entry = models.Item(
        name=entry.name, price=entry.price, date=entry.date)
    db.add(item_entry)
    db.commit()
    db.refresh(item_entry)
    return item_entry


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
