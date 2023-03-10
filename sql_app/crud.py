from sqlalchemy.orm import Session

from . import models, schemas

def get_item_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemEntry).offset(skip).limit(limit).all()


def add_item_entry(db: Session, entry: schemas.ItemEntry):
    item_entry = models.Item(name=entry.name, price=entry.price, date=entry.date)
    db.add(item_entry)
    db.commit()
    db.refresh(item_entry)
    return item_entry
