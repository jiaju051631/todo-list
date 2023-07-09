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

# Link the login_manager
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(github_blueprint, url_prefix="/github_login")
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")
app.register_blueprint(task_blueprint, url_prefix="/task")


def create_production_app():
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def create_test_app():
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_TEST_DATABASE_URI
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


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
    create_production_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        ssl_context=(config.SSL_CERT, config.SSL_KEY)
    )
