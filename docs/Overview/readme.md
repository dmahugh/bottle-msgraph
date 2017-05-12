# Overview

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

## Source Files

The following is a high-level overview of the contents of this repo.

### app.py

This is the main application launcher &mdash; to run the app, run this program. Depending on how you've installed and configured Python on your system, you'll run it with one of these commands:

```python app.py
python3 app.py
py -3 app.py
```

This is boilerplate Bottle code, with the sole exception of the ```import routes``` command, which imports the route handlers from routes.py.

### routes.py

This program contains all of the route handlers. The standard Bottle decorators are used: ```@route()``` to specify which route is being handled, ```@view()``` to specify which template to use, and then a function that returns a dictionary of values to pass to the template.

### oauth2mgr.py

This file contains the definition of the ```OAuth2Manager``` class, which handles OAuth 2.0 authentication via Azure Active Directory. It includes methods for login/logout, making authenticated API calls, and managing the caching of tokens and related metadata. [See here for more information about OAuth2Manager.](../OAuth2Manager/readme.md)

## Folders

### views

This folder contains the templates for each of the rendered pages.

/// .tpl, HTML plus Python code delimited by %

/// note @view()

/// what is Bottle's template engine?

### static

The ```static``` folder contains static assets used by the app, and has subfolders for CSS files, fonts, image files, and JavaScript scripts. Note that Bootstrap and JQuery are included.

### docs

All of the documentation content. This page, for example.
