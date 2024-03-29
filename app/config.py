import os


# Get config mode
def get_config_mode():
    
    config_dict = {
        "development" : DevelopmentConfig,
        "production" : ProductionConfig
    }
    
    config_class = config_dict[os.environ.get("FLASK_ENV")]
    
    return config_class


class Config:
    # Flask configurations
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_KEY = os.urandom(32)
    
    # SQLAlchemy configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 180
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 180}


class DevelopmentConfig(Config):
    DB_NAME = "warranty_dev.db"
    DB_NAME_BACKUP = "warranty_dev_bkp.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    RECORDS_PER_PAGE = 3
    
    
class ProductionConfig(Config):
    DB_NAME = "warranty.db"
    DB_NAME_BACKUP = "warranty_bkp.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    # SQLALCHEMY_DATABASE_URI = "{}:///{}:{}@{}:{}/{}".format(
    #     os.environ.get("DB_ENGINE"     , "sqlite"),
    #     os.environ.get("DB_USERNAME"   , "root"),
    #     os.environ.get("DB_PASSWORD"   , ""),
    #     os.environ.get("DB_HOST"       , "localhost"),
    #     os.environ.get("DB_PORT"       , "5432"),
    #     os.environ.get("DB_NAME"       , "warranty.db")
    # )
    RECORDS_PER_PAGE = 10
    
     
     
