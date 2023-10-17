from flask import render_template
from app.main import main_bp
from app.main.forms import AddShopForm

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
    
    return render_template("shops.html",
                           title="Shops",
                           add_shop_form=add_shop_form)


@main_bp.route("/database")
def database():
    return render_template("database.html", title="Database")
