import os

from flask import Flask, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, logout_user

import config
from blueprints import google_blueprint, github_blueprint, facebook_blueprint, task_blueprint
from exts import db
from models import login_manager


# Environment variables
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = config.OAUTHLIB_RELAX_TOKEN_SCOPE
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config.OAUTHLIB_INSECURE_TRANSPORT

# Initialize Flask app with configurations
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

# Link the database
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created")

# Link the login_manager
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(github_blueprint, url_prefix="/github_login")
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")
app.register_blueprint(task_blueprint, url_prefix="/task")


# Homepage
@app.route("/")
def index():
    return render_template("home.html", current_user=current_user)

# Logout the user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context=(config.SSL_CERT, config.SSL_KEY))
