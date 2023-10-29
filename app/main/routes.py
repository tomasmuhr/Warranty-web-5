from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from sqlalchemy.orm import aliased
from app.main import main_bp
from app.main.forms import ItemForm, ShopForm
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


# --- SHOPS ---
@main_bp.route("/shops", methods=['GET', 'POST'])
def shops():
    add_shop_form = ShopForm()
    
    if "shop_form" in request.form and add_shop_form.validate_on_submit():
        shop = Shop(name=add_shop_form.name.data,
                    street=add_shop_form.street.data,
                    city=add_shop_form.city.data,
                    zip_code=add_shop_form.zip_code.data)
        
        db.session.add(shop)
        db.session.commit()
        
        flash("The record has been successfully added!", category="success")
        
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


@main_bp.route("/edit_shop/<int:shop_id>", methods=['GET', 'POST'])
def edit_shop(shop_id: int):
    shop = Shop.query.filter_by(id=shop_id).first()
    edit_shop_form = ShopForm()
    
    if request.method == "POST":
        if "shop_form" in request.form and edit_shop_form.is_submitted():
            edit_shop_form.populate_obj(shop)
            
            db.session.commit()
             
            flash("The record has been successfully edited.", category="success")
            
            return redirect(url_for("main.shops"))
    
    return redirect(url_for("main.shops"))
    

@main_bp.route("/delete_shop/<int:shop_id>", methods=['GET'])
def delete_shop(shop_id: int):
    shop = Shop.query.filter_by(id=shop_id).first()
    
    db.session.delete(shop)
    db.session.commit()
    
    flash("The record has been successfully deleted.", category="success")
    
    return redirect(url_for("main.shops"))


# --- ITEMS ---
@main_bp.route("/items", methods=['GET', 'POST'])
def items():
    shops = Shop.query.all()
    shop_choices = [(int(shop.id), shop.name) for shop in shops]
    shop_choices = sorted(shop_choices, key=lambda x: x[1])
    
    add_item_form = ItemForm(shop_choices)
    
    if request.method == "POST":
        if "item_form" in request.form and add_item_form.submit():
            item = Item(name=add_item_form.name.data,
                        receipt_nr=add_item_form.receipt_nr.data,
                        amount=add_item_form.amount.data,
                        price_per_piece=add_item_form.price_per_piece.data,
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
            
            flash("The record has been successfully added.", category="success")
            
            return redirect(url_for("main.items"))
        
        else:
            flash("Something went wrong.", category="danger")
            print(add_item_form.errors)
    
    item_rows = db.session \
        .query(Item, Dates) \
        .outerjoin(Dates) \
        .all()
        
    return render_template("items.html",
                           title="Items",
                           add_item_form=add_item_form,
                           item_rows=item_rows)
    
    
@main_bp.route("/edit_item/<int:item_id>", methods=['GET', 'POST'])
def edit_item(item_id: int):
    edit_item_form = ItemForm()
    
    if "item_form" in request.form and edit_item_form.is_submitted():
        item = Item.query.filter_by(id=item_id).first()
        
        item.name = edit_item_form.name.data
        item.receipt_nr = edit_item_form.receipt_nr.data
        item.amount = edit_item_form.amount.data
        item.price_per_piece = edit_item_form.price_per_piece.data
        item.comment = edit_item_form.comment.data
        item.shop_id = edit_item_form.shop.data
        # TODO purchase date and w
        
        db.session.update(item)
        db.session.commit()
        
        flash("The record has been successfully edited.", category="success")
        
        return redirect(url_for("main.items"))
    
    return redirect(url_for("main.items"))
    

@main_bp.route("/delete_item/<int:item_id>", methods=['GET'])
def delete_item(item_id: int):
    item = Item.query.filter_by(id=item_id).first()
    
    db.session.delete(item)
    db.session.commit()
    
    flash("The record has been successfully deleted.", category="success")
    
    return redirect(url_for("main.items"))


# DATABASE
@main_bp.route("/database")
def database():
    return render_template("database.html", title="Database")


# SEARCH
@main_bp.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    
    item_alias = aliased(Item)
    items = db.session.query(item_alias, Dates) \
                    .outerjoin(Dates) \
                    .filter(item_alias.name.ilike(f"%{query}%")) \
                    .all()
    
    shop_alias = aliased(Shop)
    shops = db.session.query(shop_alias, func.count(Item.id)) \
                    .outerjoin(Item) \
                    .group_by(shop_alias.id) \
                    .filter(shop_alias.name.ilike(f"%{query}%")) \
                    .all()
    
    return render_template("search.html",
                           title="Search Results",
                           search_query=query,
                           search_result_items=items,
                           search_result_shops=shops)


