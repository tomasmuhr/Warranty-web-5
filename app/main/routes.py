from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import distinct, func, or_
from sqlalchemy.orm import aliased
from app.main import main_bp
from app.main.forms import AddItemForm, ShopForm
from app.models import Date, Item, Shop
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
            
            get_record_count(Shop)
            
            flash("The record has been successfully added!", category="success")
            
            return redirect(url_for("main.shops"))
        
        else:
            flash("Something went wrong. The shop name probably already exists or is empty. Please try again.",
                  category="danger")
            
            print_error_messages(add_shop_form)

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
            # if any([edit_shop_form.name.data.lstrip() == shop.name and edit_shop_form.is_submitted(),
                    # edit_shop_form.name.data.lstrip() != shop.name and edit_shop_form.validate_on_submit()]):
            
            # Remove leading spaces
            edit_shop_form.name.data = edit_shop_form.name.data.lstrip()
            new_name = edit_shop_form.name.data
            
            # A if the name is the same - proceed
            if new_name == shop.name:
                # print(new_name)
                # print("The name is the same")
                edit_shop_form.populate_obj(shop)
            
                db.session.commit()
                
                flash("The record has been successfully updated.", category="success")
            
            # B if the name is not the same - check if a shop with the same name exists
            elif new_name != shop.name:
                # print(new_name)
                
                check_result = db.session.execute(
                    db.select(Shop.name)
                    .where(Shop.name == new_name)
                ).scalar()
                # print(check_result)
                
                if not check_result:
                    # print("The shop name is not in use, ok")
                    edit_shop_form.populate_obj(shop)
                    
                    db.session.commit()
                    
                    flash("The record has been successfully updated.", category="success")
                    
                else:
                    # print("The shop name probably already exists or is empty")
                    flash("The shop name probably already exists or is empty. Please try again.",
                          category="danger")
                    
                    print_error_messages(edit_shop_form)
                
            else:
                flash("Something went wrong. The shop name probably already exists or is empty. Please try again.",
                        category="danger")
                
                print_error_messages(edit_shop_form)
        
        
        return redirect(url_for("main.shops"))

    # just for case when the form is not submitted
    return redirect(url_for("main.shops"))
            

@main_bp.route("/delete_shop/<int:shop_id>", methods=['GET'])
def delete_shop(shop_id: int):
    db.session.execute(
        db.delete(Shop)
        .where(Shop.id == shop_id)
    )
    # TODO delete linked items?
    
    db.session.commit()
    
    get_record_count(Shop)

    flash("The record has been successfully deleted.", category="success")
    
    return redirect(url_for("main.shops"))


# --- ITEMS ---
# TODO add BLOB for adding user images?
@main_bp.route("/items", methods=['GET', 'POST'])
def items():
    # Get shop choices for select shop field
    shop_choices = get_shop_choices()
    
    # Get shop info for shop view modal
    items_shops_dict = {}
    items_shops = db.session.execute(
        db.select(Item.id, Shop)
        .outerjoin(Shop)
    ).fetchall()
    
    for item_shop in items_shops:
        items_shops_dict[item_shop[0]] = item_shop[1]
    
    # Add shop_choices to form to initialize shop choices
    add_item_form = AddItemForm(shop_choices)
    
    if request.method == "POST":
        if "add_item_form" in request.form and add_item_form.validate_on_submit():
            shop_id = db.session.execute(
                db.select(Shop.id)
                .where(Shop.name == add_item_form.shop.data)
            ).scalar()

            # ! orphans - dates connect to the appropriate item and this renders multiple times
            item = Item(name=add_item_form.name.data,
                        receipt_nr=add_item_form.receipt_nr.data,
                        amount=add_item_form.amount.data,
                        price_per_piece=add_item_form.price_per_piece.data,
                        comment=add_item_form.comment.data,
                        shop_id=shop_id)
            
            date = Date(item_id=item.id,
                        purchase_date=add_item_form.purchase_date.data,
                        warranty_months=add_item_form.warranty_months.data,
                        expiration_date=add_item_form.purchase_date.data + \
                            relativedelta(months=add_item_form.warranty_months.data))
            
            item.date.append(date)
            
            db.session.add(item)
            db.session.commit()
            
            get_record_count(Item, Date)
            
            flash("The record has been successfully added.", category="success")
            
            return redirect(url_for("main.items"))
        
        else:
            flash("Something went wrong.", category="danger")
            
            print_error_messages(add_item_form)
    
    item_rows = db.session.execute(
        db.select(Item, Date, Shop.name)
        .outerjoin(Date)
        .outerjoin(Shop)
    ).fetchall()
    
    print(item_rows)
        
    return render_template("items.html",
                           title="Items",
                           add_item_form=add_item_form,
                           item_rows=item_rows,
                           shop_choices=shop_choices,
                           items_shops = items_shops_dict)
    
    
@main_bp.route("/edit_item/<int:item_id>", methods=['GET', 'POST'])
def edit_item(item_id: int):
    item = db.session.execute(
        db.select(Item)
        .where(Item.id == item_id)
    ).fetchone()[0]
    
    date = db.session.execute(
        db.select(Date)
        .where(Date.item_id == item_id)
    ).fetchone()[0]
    
    # Form returns strings for all fields - need conversion
    item.name = request.form.get("name")
    item.receipt_nr = request.form.get("receipt_nr")
    item.comment = request.form.get("comment")
    
    # Get shop_id by shop name
    shop_id = db.session.execute(
        db.select(Shop.id)
        .where(Shop.name == request.form.get("shop"))
    ).scalar()
    
    item.shop_id = shop_id
    
    # Check amount
    amount = request.form.get("amount")
    if amount:
        item.amount = request.form.get("amount")
    else:
        item.amount = None
    
    # Check float value in price_per_piece
    price_per_piece = request.form.get("price_per_piece")
    if price_per_piece:
        item.price_per_piece = price_per_piece
    else:
        item.price_per_piece = None
    
    date.warranty_months = request.form.get("warranty_months")
    # Convert purchase_date to datetime - to be able to create
    # a new datetime object by relativedelta
    purchase_date_str = request.form.get("purchase_date")
    date.purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
    date.expiration_date = date.purchase_date + \
        relativedelta(months=int(date.warranty_months))
    
    db.session.commit()
    
    flash("The record has been successfully edited.", category="success")
    
    return redirect(url_for("main.items"))
    

@main_bp.route("/delete_item/<int:item_id>", methods=['GET'])
def delete_item(item_id: int):
    db.session.execute(
        db.delete(Item)
        .where(Item.id == item_id)
    )
    
    # ! workaround for cascade delete
    db.session.execute(
        db.delete(Date)
        .where(Date.item_id == item_id)
    )
    
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
                    
    shop_choices = get_shop_choices()
                    
    items = db.session.execute(
        db.select(Item, Date, Shop.name)
        .outerjoin(Date)
        .outerjoin(Shop)
        .where(or_(Item.name.ilike(f"%{query}%"),
                   Item.comment.ilike(f"%{query}%")))
        .order_by(Item.name)
    ).fetchall()
    
    shops = db.session.execute(
        db.select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .where(Shop.name.ilike(f"%{query}%"))
        .group_by(Shop)
        .order_by(Shop.name)
    ).fetchall()
    
    return render_template("search.html",
                           title="Search Results",
                           search_query=query,
                           shop_choices=shop_choices,
                           search_result_items=items,
                           search_result_shops=shops)


# UTILITIES
def get_record_count(*args):
    results_dict = {}
    
    for a in args:
        rslt = db.session.execute(
            db.select(func.count(a.id))
        ).scalar()
        
        results_dict[a] = rslt
    
    for key, value in results_dict.items():
        print(f"{key.__name__}: {value} records")
        
        
def print_error_messages(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f'{field}: {error}')
    print( ', '.join(error_messages))

    
def get_shop_choices():
    shop_choices_temp = db.session.execute(
        db.select(Shop.name)
        .order_by(func.lower(Shop.name))
    ).fetchall()
    
    shop_choices = [shop[0] for shop in shop_choices_temp]
    
    return shop_choices