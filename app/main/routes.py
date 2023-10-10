from flask import render_template
from app.main import main_bp

@main_bp.route("/", methods=['GET', 'POST'])
@main_bp.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="Home")
    

@main_bp.route("/about")
def about():
    # update also in footer
    versions = (
        "1.0 - initial version",
        )
    return render_template("about.html", title="About", versions=versions)

