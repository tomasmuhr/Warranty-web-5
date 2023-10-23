import csv
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from sqlalchemy import column
from app.config import get_config_mode
from dateutil.relativedelta import relativedelta


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()

load_dotenv(".env")


# Check environment
if os.environ.get("FLASK_ENV") == "production" and os.environ.get("FLASK_DEBUG") == "1":
    exit("FLASK_DEBUG cannot be set to 1 in production mode")
else:
    # Get config class for create_app() function
    config_class = get_config_mode()


# Create app
def create_app(config_class=config_class):
    app = Flask(__name__)
    
    app.config.from_object(config_class) 
   
    db.init_app(app) 
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    
    register_blueprints(app)
    register_logging(app)
    configure_database(app)
    
    return app


def register_blueprints(app):
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)
    

def register_logging(app):
    logs_path = Path("logs")
    
    if not logs_path.exists():
        logs_path.mkdir()

    file_handler = RotatingFileHandler("logs/warranty_web.log",
                                        maxBytes=10240,
                                        backupCount=10)

    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler) 
    
    app.logger.setLevel(logging.INFO)
    app.logger.info("Warranty-web startup") 
    app.logger.info(f"App mode: {os.environ.get('FLASK_ENV')}")
    app.logger.info(f"Debug mode: {os.environ.get('FLASK_DEBUG')}")
    app.logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    
def configure_database(app):
    with app.app_context():
        db.create_all()
        
        # Load fake data
        app_mode = os.environ.get("FLASK_ENV")
        
        if app_mode == "development":
            # FAKE SHOPS
            db_shops_count = db.session.query(column("Shop")).count()
            app.logger.info(f"Fake shops count: {db_shops_count}")
        
            if db_shops_count <= 1:
                csv_path = Path("app/data/fake_shops.csv")
                
                if csv_path.exists():
                    with open(csv_path, "r", encoding="utf-8") as f:
                        csv_reader = csv.DictReader(f)
                        
                        for row in csv_reader:
                            new_shop = Shop(name=row["name"],
                                            street=row["street"],
                                            city=row["city"],
                                            zip_code=row["zip"])
                            
                            db.session.add(new_shop)
                            
                        db.session.commit()
                        
                    # delete abundant shops
                    db.session.query(Shop).filter(Shop.id > 20).delete()
                    db.session.commit()
                    app.logger.info("Fake shops filled.")
            else:
                app.logger.info("Fake shops in database already filled.")
                
            # FAKE ITEMS
            db_items_count = db.session.query(column("Item")).count()
            app.logger.info(f"Fake items count: {db_items_count}")
            
            if db_items_count <= 1:
                csv_path = Path("app/data/fake_items.csv")
                
                if csv_path.exists():
                    with open(csv_path, "r", encoding="utf-8") as f:
                        csv_reader = csv.DictReader(f)
                        
                        for row in csv_reader:
                            new_item = Item(name=row["name"],
                                            receipt_nr=row["receipt_nr"],
                                            amount=row["amount"],
                                            price_per_piece=row["price"],
                                            comment=row["comment"],
                                            shop_id=row["shop_id"])
                            
                            db.session.add(new_item)
                            
                        db.session.commit()
                        
                    # delete abundant items
                    db.session.query(Item).filter(Item.id > 46).delete()
                    db.session.commit()
                    app.logger.info("Fake items filled.")
                    
            else:
                app.logger.info("Fake items in database already filled.")
                    
            # FAKE DATES
            db_dates_count = db.session.query(column("Dates")).count()
            app.logger.info(f"Fake dates count: {db_dates_count}")
            
            if db_dates_count <= 1:
                csv_path = Path("app/data/fake_dates.csv")
                
                if csv_path.exists():
                    with open(csv_path, "r", encoding="utf-8") as f:
                        csv_reader = csv.DictReader(f)
                        
                        for row in csv_reader:
                            p_date = datetime.strptime(row["purchase_date"], "%Y-%m-%d")
                            
                            new_dates = Dates(item_id=row["item_id"],
                                              warranty_months=row["warranty_months"],
                                              purchase_date = p_date,
                                              expiration_date=p_date + relativedelta(months=int(row["warranty_months"])))
                            
                            db.session.add(new_dates)
                            
                        db.session.commit()
                    
                    # delete abundant dates
                    db.session.query(Dates).filter(Dates.id > 46).delete()
                    db.session.commit()
                    app.logger.info("Fake dates filled.")
                    
            else:
                app.logger.info("Fake dates in database already filled.")
                    

    @app.teardown_request
    def remove_database_session(exception=None):
        db.session.remove()


from app.models import Dates, Item, Shop
