from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from app.main import main_bp
from app.main.forms import AddItemForm, AddShopForm
from app.models import Dates, Item, Shop
from app import db
from dateutil.relativedelta import relativedelta


@main_bp.route("/", methods=['GET'])
@main_bp.route("/index", methods=['GET'])
def index():
    return render_template("index.html", title="Home")
    

@main_bp.route("/about")
def about():
    versions = (
        "1.0 - initial version",
        )
    return render_template("about.html", title="About", versions=versions)


@main_bp.route("/items", methods=['GET', 'POST'])
def items():
    add_item_form = AddItemForm()

    if "add_item" in request.form and add_item_form.validate_on_submit():
        print("je tam")
        item = Item(name=add_item_form.name.data,
                    receipt_nr=add_item_form.receipt_nr.data,
                    amount=add_item_form.amount.data if add_item_form.amount.data else 0,
                    price_per_piece=add_item_form.price_per_piece.data if add_item_form.price_per_piece.data else 0.0,
                    comment=add_item_form.comment.data,
                    shop_id=add_item_form.shop.data)
        
        dates = Dates(item_id=item.id,
                      purchase_date=add_item_form.purchase_date.data,
                      warranty_months=add_item_form.warranty_months.data,
                      expiration_date=add_item_form.purchase_date.data + \
                          relativedelta(months=add_item_form.warranty_months.data))
        
        item.dates.append(dates)
        
        db.session.add(item)
        db.session.commit()
        
        flash("Item successfully added!", category="success")
        
        return redirect(url_for("main.items"))
    
    else:
        print("nie je tam")

    item_rows = db.session \
        .query(Item, Dates) \
        .outerjoin(Dates) \
        .all()
        
    return render_template("items.html",
                           title="Items",
                           add_item_form=add_item_form,
                           item_rows=item_rows)


@main_bp.route("/shops", methods=['GET', 'POST'])
def shops():
    add_shop_form = AddShopForm()
    
    if "add_shop" in request.form and add_shop_form.validate_on_submit():
        shop = Shop(name=add_shop_form.name.data,
                    street=add_shop_form.street.data if add_shop_form.street.data else "n/a",
                    city=add_shop_form.city.data if add_shop_form.city.data else "n/a",
                    zip_code=add_shop_form.zip_code.data if add_shop_form.zip_code.data else "n/a")
        
        db.session.add(shop)
        db.session.commit()
        
        flash("Shop successfully added!", category="success")
        
        return redirect(url_for("main.shops"))
    
    shop_rows = db.session \
        .query(Shop, func.count(Item.id)) \
        .outerjoin(Item) \
        .group_by(Shop.id) \
        .all()
    
    return render_template("shops.html",
                           title="Shops",
                           add_shop_form=add_shop_form,
                           shop_rows=shop_rows)


@main_bp.route("/database")
def database():
    return render_template("database.html", title="Database")
