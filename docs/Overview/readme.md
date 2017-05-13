# Overview

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

The following is a quick tour of the contents of this repo.

## app.py

The [app.py](https://github.com/dmahugh/bottle-msgraph/blob/master/app.py) source file is the main application launcher. It's boilerplate Bottle code, with the sole exception of the ```import routes``` command, which imports the route handlers from ```routes.py```.

## routes.py

The [routes.py](https://github.com/dmahugh/bottle-msgraph/blob/master/routes.py) source file contains the function definitions for all of the routes handled by the application, such as ```/login```, ```/logout```, and ```/sendmail```.

Note that an instance of ```OAuth2Manager``` named ```msgraphapi``` is created at the top of the file:

```python
import oauth2mgr
msgraphapi = oauth2mgr.OAuth2Manager()
```
The ```msgraphapi``` object tracks authentication state and provides methods for handling login, logout, and authenticated calls to the Graph API.

## oauth2mgr.py

This file contains the definition of the [OAuth2Manager](../OAuth2Manager/readme.md) class, which handles OAuth 2.0 authentication via Azure Active Directory. It includes methods for login/logout, making authenticated API calls, managing the caching and refreshing of tokens, and so on.

## /views folder

This folder contains the templates for each page of the app. These are ```.tpl``` files that are rendered by Bottle's [SimpleTemplate](http://bottlepy.org/docs/dev/stpl.html) template engine. They're HTML with inline Python code on lines that begin with a ```%``` character.

Note that the ```@view()``` decorators in ```routes.py``` associate handler functions with a template. For example, the ```about()``` function has an ```@view('about')``` decorator, so the dictionary it returns is rendered by the ```about.tpl``` template.

## /static folder

The ```static``` folder contains static assets used by the app, and has subfolders for CSS files, fonts, image files, and JavaScript scripts. Note that Bootstrap and JQuery are included.

## /docs folder

All of the documentation content. This page, for example.
