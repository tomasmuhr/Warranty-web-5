from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from app.main import main_bp
from app.main.forms import AddShopForm
from app.models import Item, Shop
from app import db

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


@main_bp.route("/items")
def items():
    return render_template("items.html", title="Items")


@main_bp.route("/shops", methods=['GET', 'POST'])
def shops():
    add_shop_form = AddShopForm()
    
    if "add_shop" in request.form and add_shop_form.validate_on_submit():
        shop = Shop(name=add_shop_form.name.data,
                    street=add_shop_form.street.data,
                    city=add_shop_form.city.data,
                    zip_code=add_shop_form.zip_code.data)
        db.session.add(shop)
        db.session.commit()
        
        flash("Shop successfully added!", category="success")
        
        return redirect(url_for("main.shops"))
    
    shop_rows = db.session \
        .query(Shop, func.sum(Item.amount)) \
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
