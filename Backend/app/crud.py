# app/crud.py
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models

def create_item(db: Session, item):
    """Insert a new Item row and return it."""
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 50, filters: dict | None = None):
    """Fetch items with optional filters and pagination."""
    q = db.query(models.Item)
    if filters:
        for key, value in filters.items():
            if value is not None:
                q = q.filter(getattr(models.Item, key) == value)
    return (
        q.order_by(models.Item.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_item(db: Session, item_id: int):
    """Retrieve a single item by ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_stats(db: Session):
    """
    Return overall statistics:
    - accept / reject counts (case-insensitive)
    - counts grouped by type and brand
    """
    accept = (
        db.query(func.count(models.Item.id))
        .filter(func.lower(models.Item.decision) == "accept")
        .scalar()
        or 0
    )
    reject = (
        db.query(func.count(models.Item.id))
        .filter(func.lower(models.Item.decision) == "reject")
        .scalar()
        or 0
    )

    by_type = dict(
        db.query(models.Item.type, func.count(models.Item.id))
        .group_by(models.Item.type)
        .all()
    )

    by_brand = dict(
        db.query(models.Item.brand, func.count(models.Item.id))
        .group_by(models.Item.brand)
        .all()
    )

    return {
        "accept": int(accept),
        "reject": int(reject),
        "by_type": by_type,
        "by_brand": by_brand,
    }
