from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Settings(db.Model):
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    dark_mode: Mapped[int] = mapped_column(db.Integer)
    # id = db.Column(db.Integer, primary_key=True)
    # dark_mode = db.Column(db.Integer)


class Shop(db.Model):
    __tablename__ = "shop"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), unique=True, nullable=False)
    street: Mapped[str] = mapped_column(db.String(150))
    city: Mapped[str] = mapped_column(db.String(64))
    zip_code: Mapped[str] = mapped_column(db.String(10))
    items: Mapped[List["Item"]] = db.relationship()
    # for bi-directional relationship
    # items: Mapped[List["Item"]] = db.relationship(back_populates="shop")

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), unique=True, nullable=False)
    # street = db.Column(db.String(150))
    # city = db.Column(db.String(64))
    # zip_code = db.Column(db.String(10))
    # items = db.relationship("Item", backref="shop")


class Item(db.Model):
    __tablename__ = "item"
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    receipt_nr: Mapped[str] = mapped_column(db.String(20))
    amount: Mapped[int] = mapped_column(db.Integer)
    price_per_piece: Mapped[float] = mapped_column(db.Float)
    comment: Mapped[str] = mapped_column(db.String(255))
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    dates: Mapped[List["Dates"]] = relationship()
    # for bi-directional relationship
    # shop: Mapped["Shop"] = relationship(back_populates="items")
    
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), nullable=False)
    # receipt_nr = db.Column(db.String(20))
    # amount = db.Column(db.Integer)
    # price_per_piece = db.Column(db.Float)
    # comment = db.Column(db.String(255))
    # shop_id = db.Column(db.Integer, db.ForeignKey("shop.id", name="fk_item_shop_id"))
    # # image_path = db.Column(db.LargeBinary)
    # dates = db.relationship("Dates", backref="item")

class Dates(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    warranty_months: Mapped[int] = mapped_column(db.Integer, nullable=False)
    purchase_date: Mapped[datetime.date] = mapped_column(db.Date(), nullable=False)
    expiration_date: Mapped[datetime.date] = mapped_column(db.Date(), nullable=False)
    
    # id = db.Column(db.Integer, primary_key=True)
    # item_id = db.Column(db.Integer, db.ForeignKey("item.id", name="fk_dates_item_id"), nullable=False)
    # warranty_months = db.Column(db.Integer, nullable=False)
    # purchase_date = db.Column(db.Date(), nullable=False)
    # expiration_date = db.Column(db.Date(), nullable=False)

        