# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap5

# app = Flask(__name__)

# bootstrap = Bootstrap5(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run()

from app import create_app, db
from app.models import Item, Settings, Shop


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {"db": db,
            "Settings": Settings,
            "Shop": Shop,
            "Item": Item}