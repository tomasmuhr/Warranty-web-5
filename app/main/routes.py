from datetime import datetime
from pathlib import Path
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from flask import current_app, flash, g, redirect, render_template, request, send_file, send_from_directory, url_for
from sqlalchemy import distinct, func, or_, outerjoin
from sqlalchemy.orm import aliased, lazyload
from sqlalchemy.util import ellipses_string
from app.main import main_bp
from app.main.forms import AddItemForm, ShopForm
from app.models import Date, Item, Shop
from app import db
from dateutil.relativedelta import relativedelta


@main_bp.route("/", methods=['GET'])
@main_bp.route("/index", methods=['GET'])
def index():
    items_count = db.session.execute(
        db.select(func.count(Item.id))
    ).scalar()
    
    shops_count = db.session.execute(
        db.select(func.count(Shop.id))
    ).scalar()

    return render_template("index.html", title="Home",
                           items_count=items_count,
                           shops_count=shops_count)
    

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
            shop_name_stripped = add_shop_form.name.data.strip()
            
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

    # shop_rows = db.session.execute(
    #     db.select(Shop, func.count(Item.id).label("items_count"))
    #     .outerjoin(Item, Shop.id == Item.shop_id)
    #     .group_by(Shop)
    #     .order_by(Shop.id)
    # ).fetchall()
    
    # shop_query = db.select(Shop, func.count(Item.id).label("items_count")) \
    # .outerjoin(Item, Shop.id == Item.shop_id) \
    # .group_by(Shop.id) \
    # .order_by(Shop.id)
    shop_query = db.session.query(
        Shop, func.count(Item.id).label("items_count")) \
            .outerjoin(Item) \
                .group_by(Shop.id)

    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["RECORDS_PER_PAGE"]
    shop_rows = shop_query.paginate(page=page, per_page=per_page, error_out=False)
    
    print(f"\nShop query:\n{'-'*11}\n", shop_query)
    print(f"\nFetchall():\n{'-'*11}\n", db.session.execute(shop_query).fetchall())
    print(f"\nShop rows:\n{'-'*10}\n", shop_rows)
    print(f"\nShop rows.items:\n{'-'*16}\n", shop_rows.items, "\n")
    
    # for _ in shop_rows.iter_pages():
    #     print(f"PAGE {shop_rows.page} of {shop_rows.pages}")
    #     print("-")
    #     for item in shop_rows.items:
    #         print(item[0].name, f"| items: {item[1]}")
    #     print("-")
    #     shop_rows = shop_rows.next()
    
    return render_template("shops.html",
                           title="Shops",
                           add_shop_form=add_shop_form,
                           shop_rows=shop_rows) 


@main_bp.route("/edit_shop/<int:shop_id>_<redirect_to>_<query>", methods=['GET', 'POST'])
def edit_shop(shop_id: int, redirect_to: str, query: str):
    shop = db.session.execute(
        db.select(Shop)
        .where(Shop.id == shop_id)
    ).fetchone()[0]

    # shop form to populate_obj(shop) at once
    edit_shop_form = ShopForm()
    
    if request.method == "POST":
        if "edit_shop_form" in request.form:
            # Remove trailing spaces
            shop_name_stripped = edit_shop_form.name.data.strip()
            
            if not shop_name_stripped:
                flash("Something went wrong. The shop name is probably empty. Please try again.",
                      category="danger")
                
            else:
                # A) if the name is the same - proceed
                if shop_name_stripped == shop.name:
                    edit_shop_form.name.data = shop_name_stripped
                    
                    edit_shop_form.populate_obj(shop)
                
                    db.session.commit()
                    
                    flash("The record has been successfully updated.", category="success")
                
                # B) if the name is not the same - check if a shop with the same name exists
                elif shop_name_stripped != shop.name:
                    
                    check_result = db.session.execute(
                        db.select(Shop.name)
                        .where(Shop.name == shop_name_stripped)
                    ).scalar()
                    
                    if not check_result:
                        edit_shop_form.name.data = shop_name_stripped
                        
                        edit_shop_form.populate_obj(shop)
                        
                        db.session.commit()
                        
                        flash("The record has been successfully updated.", category="success")
                        
                    else:
                        flash("The shop name probably already exists or is empty. Please try again.",
                            category="danger")
                        
                        print_error_messages(edit_shop_form)
                    
                else:
                    flash("Something went wrong. The shop name probably already exists or is empty. Please try again.",
                            category="danger")
                    
                    print_error_messages(edit_shop_form)
        
    if redirect_to == "main.search":
        return redirect(url_for(redirect_to, query=query))
    else:
        return redirect(url_for(redirect_to))


@main_bp.route("/delete_shop/<int:shop_id>_<int:linked_items>_<int:search_results>", methods=['GET'])
def delete_shop(shop_id: int, linked_items: int, search_results: int):
    db.session.execute(
        db.delete(Shop)
        .where(Shop.id == shop_id)
    )
    
    if linked_items:
        # delete linked items´s dates first
        items = db.session.execute(
            db.select(Item.id)
            .where(Item.shop_id == shop_id)
        ).fetchall()
        
        item_ids = [item[0] for item in items]
        print(f"Item_ids: {item_ids}")
        
        db.session.execute(
            db.delete(Date)
            .where(Date.item_id.in_(item_ids))
        )
        
        # then delete linked items
        db.session.execute(
            db.delete(Item)
            .where(Item.shop_id == shop_id)
        )
        
        flash_message = "The record and linked items have been successfully deleted."
        
    else:
        # clear shop_id in related items
        db.session.execute(
            db.update(Item)
            .where(Item.shop_id == shop_id)
            .values(shop_id=None)
        )
    
        flash_message = "The record has been successfully deleted."
    
    db.session.commit()
    
    flash(flash_message, category="success")
    
    if search_results:
        return redirect(url_for("main.search"))
    else:
        return redirect(url_for("main.shops"))


@main_bp.route("/shop_view_modal/<shop_id>")
def shop_view_modal(shop_id: str):
    items_expired = db.session.execute(
        db.select(Item.name, Date.purchase_date, Date.expiration_date)
        .where(Item.shop_id == shop_id)
        .join(Date, Item.id == Date.item_id)
        .where(Date.expiration_date < datetime.now())
        .order_by(Date.expiration_date.desc())
    ).fetchall()
    
    items_not_expired = db.session.execute(
        db.select(Item.name, Date.purchase_date, Date.expiration_date)
        .where(Item.shop_id == shop_id)
        .join(Date, Item.id == Date.item_id)
        .where(Date.expiration_date >= datetime.now())
        .order_by(Date.expiration_date.desc())
    ).fetchall()

    print(f"Shop_id: {shop_id}")
    print(f"Returns expired:     {items_expired}")
    print(f"Returns not expired: {items_not_expired}")
    
    return render_template("_tables_warranty_items.html",
                           items_expired=items_expired,
                           items_not_expired=items_not_expired)


# --- ITEMS ---
@main_bp.route("/items", methods=['GET', 'POST'])
def items():
    # Get shop choices for select shop field
    shop_choices = get_shop_choices()
    # Get shop info for shop view modal
    items_shops_dict = get_shops_by_items()
    # Get record count for shop view modal
    shops_items_count_dict = get_items_count_by_shops()
    print(f"Shops_items_count_dict: \n{shops_items_count_dict}")
    
    # Add form and shop_choices to initialize select field
    add_item_form = AddItemForm(shop_choices)
    
    if request.method == "POST":
        if "add_item_form" in request.form and add_item_form.validate_on_submit():
            shop_id = db.session.execute(
                db.select(Shop.id)
                .where(Shop.name == add_item_form.shop.data)
            ).scalar()

            # ! orphans - dates connect to the appropriate item and this renders multiple times
            item = Item(name=add_item_form.name.data.strip(),
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
            flash("Something went wrong. The item name is probably empty. Please try again.",
                  category="danger")
            
            print_error_messages(add_item_form)
    
    # item_query = db.select(Item.id, Item.name, Item.receipt_nr, Item.amount, Item.price_per_piece,
    #                        Item.comment, Date.purchase_date, Date.warranty_months,
    #                        Date.expiration_date, Shop.name.label("shop_name")) \
    #              .outerjoin(Date) \
    #              .outerjoin(Shop)
    item_query = db.session.query(
        Item, Date, Shop.name.label("shop_name")) \
            .outerjoin(Date) \
                .outerjoin(Shop)
    
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["RECORDS_PER_PAGE"]
    item_rows = item_query.paginate(page=page, per_page=per_page, error_out=False)

    print(f"\Item query:\n{'-'*11}\n", item_query)
    print(f"\nFetchall():\n{'-'*11}\n", db.session.execute(item_query).fetchall())
    print(f"\nItem rows:\n{'-'*10}\n", item_rows)
    print(f"\nItem rows.items:\n{'-'*16}\n", item_rows.items, "\n")
    
    return render_template("items.html",
                           title="Items",
                           add_item_form=add_item_form,
                           item_rows=item_rows,
                           shop_choices=shop_choices,
                           items_shops = items_shops_dict,
                           items_count_for_shops = shops_items_count_dict)
    
    
@main_bp.route("/edit_item/<int:item_id>_<redirect_to>_<query>", methods=['GET', 'POST'])
def edit_item(item_id: int, redirect_to: str, query: str):
    item = db.session.execute(
        db.select(Item)
        .where(Item.id == item_id)
    ).fetchone()[0]
    
    date = db.session.execute(
        db.select(Date)
        .where(Date.item_id == item_id)
    ).fetchone()[0]
    
    # Form returns strings for all fields - needs conversions!
    item_name = request.form.get("name")
    item_name_stripped = item_name.strip()
    if not item_name_stripped:
        flash("Something went wrong. The item name is probably empty. Please try again.",
              category="danger")
        
    else:
        item.name = request.form.get("name").strip()
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
    
    if redirect_to == "main.search":
        return redirect(url_for(redirect_to, query=query))
    else:
        return redirect(url_for(redirect_to))
    

@main_bp.route("/delete_item/<int:item_id>_<redirect_to>_<query>", methods=['GET'])
def delete_item(item_id: int, redirect_to: str, query: str):
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
    
    if redirect_to == "main.search":
        return redirect(url_for(redirect_to, query=query))
    else:
        return redirect(url_for(redirect_to))


# DATABASE
@main_bp.route("/database")
def database():
    db_file = db.engine.url.database
    
    return render_template("database.html", title="Database", db_file=db_file)


@main_bp.route("/db_export")
def db_export():
    db_path = Path(db.engine.url.database)
    backup_path = db_path.with_suffix(".sqlite.bkp")
    
    # Create backup of the database file
    shutil.copyfile(db_path, backup_path)

    return send_file(backup_path, as_attachment=True)


@main_bp.route("/db_purge_items")
def db_purge_items():
    print("db_purge_items")
    return render_template("database.html", title="Database")
    

@main_bp.route("/db_purge_shops")
def db_purge_shops():
    print("db_purge_shops")
    return render_template("database.html", title="Database")


# SEARCH
@main_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        query = request.args.get("query")
    else:
        query = request.form.get("query")
                    
    shop_choices = get_shop_choices()
                    
    items = db.session.execute(
        db.select(Item, Date, Shop)
        .outerjoin(Date)
        .outerjoin(Shop)
        .where(or_(Item.name.ilike(f"%{query}%"),
                   Item.comment.ilike(f"%{query}%"))
               )
        .order_by(Item.name)
    ).fetchall()
    
    shops = db.session.execute(
        db.select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .where(or_(Shop.name.ilike(f"%{query}%"),
                   Shop.street.ilike(f"%{query}%"),
                   Shop.city.ilike(f"%{query}%"))
               )
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
    """
    For debugging purposes only.
    Prints out the number of records in the database for each model.
    """
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


def get_shops_by_items():
    items_shops_dict = {}
    
    items_shops = db.session.execute(
        db.select(Item.id, Shop)
        .outerjoin(Shop)
    ).fetchall()
    
    for item in items_shops:
        items_shops_dict[item[0]] = item[1]
        
    return items_shops_dict


def get_items_count_by_shops():
    shops_items_count_dict = {}
    
    shops_items_count = db.session.execute(
        db.select(Shop, func.count(Item.id).label("items_count"))
        .outerjoin(Item, Shop.id == Item.shop_id)
        .group_by(Shop)
    ).fetchall()
    
    for shop in shops_items_count:
        shops_items_count_dict[shop[0].id] = shop[1]
        
    return shops_items_count_dict

