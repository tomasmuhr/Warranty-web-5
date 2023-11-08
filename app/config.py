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
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 180
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 180}


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI =  "sqlite:///warranty.sqlite"
    
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        os.environ.get("DB_ENGINE"     , "sqlite"),
        os.environ.get("DB_USERNAME"   , "root"),
        os.environ.get("DB_PASSWORD"   , ""),
        os.environ.get("DB_HOST"       , "localhost"),
        os.environ.get("DB_PORT"       , "5432"),
        os.environ.get("DB_NAME"       , "warranty.db")
    )
     
     
