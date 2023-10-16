from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import get_config_mode

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()

load_dotenv(".env")

# Check environment
if os.environ.get("FLASK_ENV") == "production" and os.environ.get("FLASK_DEBUG") == "1":
    exit("FLASK_DEBUG cannot be set to 1 in production mode")
else:
    # Get config class
    config_class = get_config_mode()

# Create app
def create_app(config_class=config_class):
    app = Flask(__name__)
    
    app.config.from_object(config_class) 
   
    db.init_app(app) 
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    
    register_blueprints(app)
    register_extensions(app)
    
    return app


# Helper functions
def register_blueprints(app):
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)
    

# Extension functions
def register_extensions(app):
    # File logging
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler("logs/warranty_web.log",
                                        maxBytes=10240,
                                        backupCount=10)

    file_handler.setFormatter(logging.Formatter(
        "\n%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler) 
    
    app.logger.setLevel(logging.INFO)
    app.logger.info("Warranty-web startup") 
    app.logger.info(f"App mode: {os.environ.get('FLASK_ENV')}")
    app.logger.info(f"Debug mode: {os.environ.get('FLASK_DEBUG')}")
    
      