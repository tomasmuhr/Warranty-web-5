import os
# from pathlib import Path

# current_file_path = Path(__file__).resolve()
# root_dir = current_file_path.parent.parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI =  os.environ.get("DATABASE_URL") or \
    #     "sqlite:///" + str(root_dir.joinpath("warranty.db"))
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 180
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 180}
    DEFAULT_COLOR_THEME = 1


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.environ.get("DEV_DATABASE_URL")
    
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =  os.environ.get("TEST_DATABASE_URL")
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
     
     