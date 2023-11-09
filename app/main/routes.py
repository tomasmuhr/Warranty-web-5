from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import distinct, func
from sqlalchemy.orm import aliased
from app.main import main_bp
from app.main.forms import AddItemForm, ShopForm
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
    
    if request.method == "POST":
        if "shop_form" in request.form and add_shop_form.validate_on_submit():
            shop_name_stripped = add_shop_form.name.data.lstrip()
            
            shop = Shop(name=shop_name_stripped,
                        street=add_shop_form.street.data,
                        city=add_shop_form.city.data,
                        zip_code=add_shop_form.zip_code.data)
            
            db.session.add(shop)
            db.session.commit()
            
            flash("The record has been successfully added!", category="success")
            
            return redirect(url_for("main.shops"))
        
        else:
            flash("Something went wrong. The shop name probably already exists or is empty. Please try again.",
                  category="danger")
            
            error_messages = []
            for field, errors in add_shop_form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            print( ', '.join(error_messages))
            
    shop_rows = db.session.execute(
        db.select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .group_by(Shop)
        .order_by(Shop.id)
    ).fetchall()
    
    return render_template("shops.html",
                           title="Shops",
                           add_shop_form=add_shop_form,
                           shop_rows=shop_rows)


@main_bp.route("/edit_shop/<int:shop_id>", methods=['GET', 'POST'])
def edit_shop(shop_id: int):
    shop = db.session.execute(
        db.select(Shop)
        .where(Shop.id == shop_id)
    ).fetchone()[0]

    edit_shop_form = ShopForm()
    
    if request.method == "POST":
        if "edit_shop_form" in request.form:
            if any([edit_shop_form.name.data.lstrip() == shop.name and edit_shop_form.is_submitted(),
                    edit_shop_form.name.data.lstrip() != shop.name and edit_shop_form.validate_on_submit()]):
                
                edit_shop_form.populate_obj(shop)
            
                db.session.commit()
                
                flash("The record has been successfully updated.", category="success")
                
            else:
                flash("Something went wrong. The shop name probably already exists or is empty. Please try again.",
                      category="danger")
                
                error_messages = []
                for field, errors in edit_shop_form.errors.items():
                    for error in errors:
                        error_messages.append(f'{field}: {error}')
                print( ', '.join(error_messages))
            
        return redirect(url_for("main.shops"))

    # just for case when the form is not submitted
    return redirect(url_for("main.shops"))
    
            

@main_bp.route("/delete_shop/<int:shop_id>", methods=['GET'])
def delete_shop(shop_id: int):
    db.session.execute(
        db.delete(Shop)
        .where(Shop.id == shop_id)
    )
    db.session.commit()
    
    flash("The record has been successfully deleted.", category="success")
    
    return redirect(url_for("main.shops"))


# --- ITEMS ---
# TODO add BLOB for adding user images?
@main_bp.route("/items", methods=['GET', 'POST'])
def items():
    shop_choices_temp = db.session.execute(
        db.select(Shop.name)
        .order_by(func.lower(Shop.name))
    ).fetchall()
    
    shop_choices = [shop[0] for shop in shop_choices_temp]
    
    # Add shop_choices to form to initialize shop choices
    add_item_form = AddItemForm(shop_choices)
    
    if request.method == "POST":
        if "add_item_form" in request.form and add_item_form.validate_on_submit():
            shop_id = db.session.execute(
                db.select(Shop.id)
                .where(Shop.name == add_item_form.shop.data)
            ).fetchone()[0]

            # FIXME orphans - dates connect to the appropriate item and this renders multiple times
            item = Item(name=add_item_form.name.data,
                        receipt_nr=add_item_form.receipt_nr.data,
                        amount=add_item_form.amount.data,
                        price_per_piece=add_item_form.price_per_piece.data,
                        comment=add_item_form.comment.data,
                        shop_id=shop_id)
            
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
    
    item_rows = db.session.execute(
        db.select(Item, Dates, Shop.name)
        .outerjoin(Dates)
        .outerjoin(Shop)
    ).fetchall()
        
    return render_template("items.html",
                           title="Items",
                           add_item_form=add_item_form,
                           item_rows=item_rows,
                           shop_choices=shop_choices)
    
    
@main_bp.route("/edit_item/<int:item_id>", methods=['GET', 'POST'])
def edit_item(item_id: int):
    # FIXME queries
    item = Item.query.filter_by(id=item_id).first()
    dates = Dates.query.filter_by(item_id=item_id).first()
    
    # Form returns strings for all fields - need conversion
    item.name = request.form.get("name")
    item.receipt_nr = request.form.get("receipt_nr")
    item.comment = request.form.get("comment")
    
    # Get shop_id by shop name
    shop = Shop.query.filter_by(name=request.form.get("shop")).first()
    item.shop_id = shop.id
    
    # Check amount
    amount = request.form.get("amount")
    if amount:
        item.amount = request.form.get("amount")
    else: item.amount = None
    
    # Check float value in price_per_piece
    price_per_piece = request.form.get("price_per_piece")
    if price_per_piece:
        item.price_per_piece = price_per_piece
    else:
        item.price_per_piece = None
    
    dates.warranty_months = request.form.get("warranty_months")
    # Convert purchase_date to datetime - to be able to create
    # a new datetime object by relativedelta
    purchase_date_str = request.form.get("purchase_date")
    dates.purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
    dates.expiration_date = dates.purchase_date + \
        relativedelta(months=int(dates.warranty_months))
    
    db.session.commit()
    
    flash("The record has been successfully edited.", category="success")
    
    return redirect(url_for("main.items"))
    

@main_bp.route("/delete_item/<int:item_id>", methods=['GET'])
def delete_item(item_id: int):
    db.session.execute(
        db.delete(Item)
        .where(Item.id == item_id)
    )
    
    # # workaround for cascade delete
    # db.session.execute(
    #     db.delete(Dates)
    #     .where(Dates.item_id == item_id)
    # )
    
    db.session.commit()

    # TEMP count items and dates
    items_dates_count = db.session.execute(
        db.select(func.count(distinct(Item.id)), func.count(distinct(Dates.id)))
    ).fetchone()
    print(f"Items: {items_dates_count[0]}, Dates: {items_dates_count[1]}")
    # /TEMP
    
    flash("The record has been successfully deleted.", category="success")
    
    return redirect(url_for("main.items"))


# DATABASE
@main_bp.route("/database")
def database():
    return render_template("database.html", title="Database")


# SEARCH
@main_bp.route("/search", methods=["POST"])
def search():
    # TODO queries
    query = request.form.get("query")
    shops = Shop.query.all()
    shop_choices = [(int(shop.id), shop.name) for shop in shops]
    shop_choices = sorted(shop_choices, key=lambda x: x[1])
    
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
                           shop_choices=shop_choices,
                           search_result_items=items,
                           search_result_shops=shops)


