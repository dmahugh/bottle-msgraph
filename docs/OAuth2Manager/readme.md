# OAuth2Manager class

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

This class provides methods for obtaining an authorization code and access token from Azure Active Directory, making authenticated calls to the Microsoft Graph API, and managing the caching and refreshing of access tokens and other metadata.

Limitations:

* This is _sample_ code for learning about OAuth 2.0, intended to be run locally on a test server.
* The implementation is based on the [OAuth 2.0 specification](http://www.rfc-editor.org/rfc/rfc6749.txt), but the only resource providers I've used it with are Azure AD and Microsoft Graph.
* Only one OAuth 2.0 grant type is supported: [Authorization Code Grant](https://tools.ietf.org/html/rfc6749#section-4.1), the most commonly used process flow for web apps.

Here's the relationship between OAuth2Manager and the [OAuth 2.0](http://www.rfc-editor.org/rfc/rfc6749.txt) process flow:

![Oauth2 flow](../images/oauth2flow.png)

## config_read() method

This method is called by ```__init__``` to load configuration settings from a ```config.json``` file, as covered in [Getting Started](../GettingStarted/readme.md). The config.json file should have this format:

```json
{
    "app_name": "bottle-msgraph",
    "app_id": "<value from app registration portal>",
    "app_secret": "<value from app registration portal>",
    "redirect_url": "http://localhost:5000/login/authorized",
    "scopes": [
        "User.Read",
        "Mail.Send",
        "Mail.Read",
        "Contacts.Read",
        "offline_access"],
    "api_base": "https://graph.microsoft.com/v1.0/",
    "auth_base": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token"
}
```

## login() method

This method handles authentication. In the [sample app](https://github.com/dmahugh/bottle-msgraph), we use a ```/login``` route with a ```login()``` handler function that simply calls the method:

```python
@route('/login')
def login():
    """Handler for /login endpoint."""
    msgraphapi.login(request.query.redirect or '/')
```

## authorized() method

After a successful login, Azure AD redirects the browser to the _Redirect URL_ that we provided when we registered the app in the [Application Registration Portal](https://apps.dev.microsoft.com/):

```http://localhost:5000/login/authorized```

Here's the implementation of a handler for that route in the Bottle-based sample app:

```python
@route('/login/authorized')
def authorized():
    """Handler for login/authorized route."""
    return msgraphapi.authorized()
```

The ```authorized()``` method receives the authorization grant from Azure AD and pass it to ```fetch_token()```.

## fetch_token() method

This method retrieves the access token and saves it and related information (expiration time, refresh token) to properties of the OAuth2Manager object, making it ready to handle authentication for calls to the Graph API.

## get() method, post() method

These are wrappers to HTTP Get/Put. They can take relative URLs for API endpoints (e.g., ```/organization```), and they send the current access token with each request.

They take an optional dictionary of HTTP headers, which can override or add to these default HTTP headers:

```json
{
  "User-Agent" : "bottle-msgraph/1.0",
  "Authorization" : "<access token>",
  "Accept" : "application/json",
  "Content-Type" : "application/json",
  "client-request-id" : "<guid>",
  "return-client-request-id" : "true"
}
```
If the currently cached access token is within 5 seconds of expiring (or has expired), these methods will attempt to refresh it with the current refresh token before invoking the Get/Put request.

## cache() method

This method handles caching of authentication state between sessions. It takes one of three _actions_ as an argument:

* _action='save'_ saves the current access token and related metadata to a ```cache.json``` file. If there is a profile photo available for the currently authenticated user, it is saved to a separate ```cache.photo``` file.
* _action='read' reads ```cache.json``` (if it exists) and loads the refresh token and related metadata into properties of the current OAuth2Manager instance. It also loads ```cache.photo``` if it exists.
* _action='clear'_ deletes the cache files if they exist.
