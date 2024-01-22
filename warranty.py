from app import create_app, db
from app.models import Date, Item, Settings, Shop


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {"db": db,
            "Settings": Settings,
            "Shop": Shop,
            "Item": Item,
            "Date": Date}