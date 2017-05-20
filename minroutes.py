"""Minimal example of implementing OAuth2Manager."""
import json
import os
import platform
import shutil
import socket
import sys
from pip.operations import freeze
from bottle import redirect, request, route, view

from oauth2mgr import OAuth2Manager
msgraphapi = OAuth2Manager()

@route('/')
@view('minimal')
def home():
    """Render the home page."""
    if msgraphapi.loggedin:
        # if user is authenticated, display last 10 emails from their inbox
        response = msgraphapi.get('me/mailFolders/Inbox/messages')
        return dict(data=response.json().get('value', None))
    else:
        return dict() # not authenticated, so just prompt for login

@route('/login')
def login():
    """Handler for /login endpoint - prompts user to authenticate."""
    msgraphapi.login(request.query.redirect or '/')

@route('/login/authorized')
def authorized():
    """Handler for login/authorized route. Fetches the access token, using the
    code returned by the authorization provider. Note that this is the redirect
    URL that was provided when the app was registered."""
    return msgraphapi.authorized()

@route('/logout')
def logout():
    """Handler for /logout endpoint. Clears cached user identity and
    access/refresh tokens."""
    msgraphapi.logout(request.query.redirect or '/')
