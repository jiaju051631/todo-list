from flask import flash
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.google import make_google_blueprint 
from flask_login import current_user, login_user

from exts import db
from models import User, OAuth


blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)

# Create / login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_login(blueprint, token):
    if not token:
        flash("Failed to get OAuth token from Google.", category="error")
        return False

    # Retrieve user info from Google
    user_info = blueprint.session.get("/oauth2/v2/userinfo")
    if not user_info.ok:
        flash("Failed to get user info from Google.", category="error")
        return False

    # Extract user info
    user_info_json = user_info.json()
    google_user_id = str(user_info_json["id"])
    google_user_email = str(user_info_json["email"])

    unqie_username = "{}_GG_{}".format(
        google_user_email.split('@')[0],
        google_user_id
    )

    # Find the OAuth token in the database
    oauth = OAuth.query.filter_by(
        provider=blueprint.name, 
        provider_user_id=google_user_id
    ).first()

    # Create the OAuth token if it doesn't exist
    if not oauth: 
        oauth = OAuth(
            provider=blueprint.name, 
            provider_user_id=google_user_id, 
            token=token
        ) # type: ignore

    # Find the user associated with the token in the database
    user = oauth.user

    # Create the User if it doesn't exist
    if not user:
        user = User(username=unqie_username) # type: ignore
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
    
    # Log in the user account
    login_user(user)
    flash("Successfully logged in with Google.")

    # Indicate that the backend shouldn't create the OAuth object 
    # in the database
    return False


# Notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " \
           "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

