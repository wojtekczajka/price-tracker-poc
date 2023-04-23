from sqlalchemy.orm import Session

from backend_app import models, schemas, security


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemEntry).offset(skip).limit(limit).all()


def add_item_entry(db: Session, entry: schemas.ItemEntry):
    item_entry = models.Item(
        name=entry.name, price=entry.price, date=entry.date)
    db.add(item_entry)
    db.commit()
    db.refresh(item_entry)
    return item_entry


def add_item_price(db: Session, price_entry: schemas.PriceEntry):
    item_price = models.Price(
        price=price_entry.price, date=price_entry.date, item_id=price_entry.item_id)
    db.add(item_price)
    db.commit()
    db.refresh(item_price)
    return item_price


def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_coment_to_item(db: Session, comment: schemas.CommentCreate):
    comment = models.Comment(
        text=comment.text, user_id=comment.user_id, item_id=comment.item_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_item_followers_by_user_and_item(db: Session, user_id: int, item_id: int):
    return db.query(models.ItemFollowers).filter_by(item_id=item_id, user_id=user_id).first()


def add_item_to_item_followers(db: Session, user_id: int, item_id: int):
    followed_item = get_item_followers_by_user_and_item(db=db, user_id=user_id, item_id=item_id)
    if followed_item:
        return None
    else:
        followed_item = models.ItemFollowers(item_id=item_id, user_id=user_id)
        db.add(followed_item)
        db.commit()
        db.refresh(followed_item)
        return followed_item


def remove_item_from_item_followers(db: Session, user_id: int, item_id: int):
    followed_item = get_item_followers_by_user_and_item(db=db, user_id=user_id, item_id=item_id)
    if followed_item:
        db.delete(followed_item)
        db.commit()
        return followed_item
    else:
        return None


def get_items_followed_by_user(db: Session, user_id: int):
    return db.query(models.ItemFollowers).filter_by(user_id=user_id).all()

