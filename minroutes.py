"""Minimal example of implementing OAuth2Manager."""
from bottle import request, route, view

import oauth2mgr

MSGRAPHAPI = oauth2mgr.OAuth2Manager(config={"configfile": "config.json"})


@route("/")
@view("minimal")
def home():
    """Render the home page."""
    if MSGRAPHAPI.loggedin:
        # if user is authenticated, display last 10 emails from their inbox
        response = MSGRAPHAPI.get("me/mailFolders/Inbox/messages")
        return dict(data=response.json().get("value", None))

    return dict()  # not authenticated, so just prompt for login


@route("/login")
def login():
    """Handler for /login endpoint - prompts user to authenticate."""
    MSGRAPHAPI.login(request.query.redirect or "/")


@route("/login/authorized")
def authorized():
    """Handler for login/authorized route. Fetches the access token, using the
    code returned by the authorization provider. Note that this is the redirect
    URL that was provided when the app was registered."""
    return MSGRAPHAPI.authorized()


@route("/logout")
def logout():
    """Handler for /logout endpoint. Clears cached user identity and
    access/refresh tokens."""
    MSGRAPHAPI.logout(request.query.redirect or "/")
