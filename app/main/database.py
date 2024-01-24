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
    try:
        print("Importing data ...")
        conn = sqlite3.connect(current_app.config["DB_NAME"])
        cursor = conn.cursor()
        print(f"Connected to {current_app.config['DB_NAME']}.")
        
        query = (f"""
                 ATTACH DATABASE '{current_app.config['DB_NAME_BACKUP']}' AS backup;
                 INSERT INTO item SELECT * FROM backup.item;
                 SELECT * FROM item;
                 DETACH DATABASE backup;
                 """)
                            
        cursor.executescript(query)
        conn.commit()
        cursor.close()
        
        print("Imported.")
        
    except sqlite3.Error as error:
        print("Failed!", error)
    finally:
        if conn:
            conn.close()
            print("Connection closed.")