from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Settings(db.Model):
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    dark_mode: Mapped[int] = mapped_column(db.Integer)


class Shop(db.Model):
    __tablename__ = "shop"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), unique=True, nullable=False)
    street: Mapped[str] = mapped_column(db.String(150))
    city: Mapped[str] = mapped_column(db.String(64))
    zip_code: Mapped[str] = mapped_column(db.String(10))
    items: Mapped[List["Item"]] = db.relationship()


class Item(db.Model):
    __tablename__ = "item"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64))
    receipt_nr: Mapped[str] = mapped_column(db.String(20))
    amount: Mapped[Optional[int]] = mapped_column(db.Integer)
    price_per_piece: Mapped[Optional[float]] = mapped_column(db.Float)
    comment: Mapped[str] = mapped_column(db.String(255))
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    # FIXME orphans - does not delete orphan
    # dates: Mapped[List["Dates"]] = relationship("Dates", backref="item",
    #                                             cascade="all", passive_deletes=True)
    dates: Mapped[List["Dates"]] = relationship("Dates", backref="item")


class Dates(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    warranty_months: Mapped[int] = mapped_column(db.Integer, nullable=False)
    purchase_date: Mapped[datetime.date] = mapped_column(db.Date(), nullable=False)
    expiration_date: Mapped[datetime.date] = mapped_column(db.Date(), nullable=False)
    