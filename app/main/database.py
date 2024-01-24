import sqlite3

from flask import current_app
from app import db


def drop_tables():
    print("Dropping tables ...")
    db.drop_all()
    print("Dropped.")
    
    
def create_tables():
    print("Creating tables ...")
    db.create_all()
    print("Created.")
    
    
def import_data():
    print("Importing data ...")
    backup_conn = sqlite3.connect(current_app.config["DB_NAME_BACKUP"])
    print(backup_conn)
    print("Imported.")