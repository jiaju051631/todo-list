from flask import flash
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import make_github_blueprint
from flask_login import current_user, login_user

from exts import db
from models import User, OAuth


blueprint = make_github_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# Create / login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def github_login(blueprint, token):
    if not token:
        flash("Failed to get OAuth token from GitHub.", category="error")
        return False

    # Retrieve user info and email from GitHub
    user_info = blueprint.session.get("/user")
    if not user_info.ok:
        flash("Failed to get user info from GitHub.", category="error")
        return False
    
    user_email = blueprint.session.get("/user/emails")
    if not user_email.ok:
        flash("Failed to get user email from GitHub.", category="error")
        return False

    # Extract user info
    user_info_json = user_info.json()
    user_email_json = user_email.json()
    github_user_id = str(user_info_json["id"])
    github_user_email = str(user_email_json[0]['email'])

    unqie_username = "{}_GH_{}".format(
        github_user_email.split('@')[0],
        github_user_id
    )

    # Find the OAuth token in the database
    oauth = OAuth.query.filter_by(
        provider=blueprint.name, 
        provider_user_id=github_user_id
    ).first()

    # Create the OAuth token if it doesn't exist
    if not oauth: 
        oauth = OAuth(
            provider=blueprint.name, 
            provider_user_id=github_user_id, 
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
    flash("Successfully logged in with GitHub.")

    # Indicate that the backend shouldn't create the OAuth object
    # in the database
    return False


# Notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def github_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " \
           "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
