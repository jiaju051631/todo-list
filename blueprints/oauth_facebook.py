from flask import flash
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_login import current_user, login_user

from exts import db
from models import User, OAuth


blueprint = make_facebook_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# Create / login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def facebook_login(blueprint, token):
    if not token:
        print("Failed to get OAuth token from Facebook.")
        return False

    # Retrieve user info from Facebook
    user_info = blueprint.session.get("/me")
    if not user_info.ok:
        flash("Failed to get user info from Facebook.", category="error")
        return False
    
    # Extract user info
    user_info_json = user_info.json()
    facebook_user_name = user_info_json['name']
    facebook_user_id = user_info_json['id']

    unqie_username = "{}_FB_{}".format(
        facebook_user_name.lower().replace(' ', '.'),
        facebook_user_id,
    )

    # Find the OAuth token in the database
    oauth = OAuth.query.filter_by(
        provider=blueprint.name, 
        provider_user_id=facebook_user_id
    ).first()

    # Create the OAuth token if it doesn't exist
    if not oauth: 
        oauth = OAuth(
            provider=blueprint.name, 
            provider_user_id=facebook_user_id, 
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
    flash("Successfully logged in with Facebook.")

    # Indicate that the backend shouldn't create the OAuth object
    #  in the database
    return False


# Notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " \
           "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")