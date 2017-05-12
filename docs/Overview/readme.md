# Overview

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

The following is a high-level overview of the contents of this repo.

## app.py

This is the main application launcher. It's boilerplate Bottle code, with the sole exception of the ```import routes``` command, which imports the route handlers from ```routes.py```.

Depending on how you've installed and configured Python on your system, use one of these commands to start the application:

```
python app.py
python3 app.py
py -3 app.py
```

## routes.py

This program contains all of the route handlers. The standard Bottle decorators are used: ```@route()``` to specify which route is being handled, ```@view()``` to specify which template to use, and then a function that returns a dictionary of values to pass to the template.

## oauth2mgr.py

This file contains the definition of the [OAuth2Manager](../OAuth2Manager/readme.md) class, which handles OAuth 2.0 authentication via Azure Active Directory. It includes methods for login/logout, making authenticated API calls, and managing the caching of tokens and related metadata.

## /views folder

This folder contains the templates for each page of the app. These are ```.tpl``` files that are rendered by Bottle's [SimpleTemplate](http://bottlepy.org/docs/dev/stpl.html) template engine. They're HTML with inline Python code on lines that begin with a ```%``` character.

Note that the ```@view()``` decorators in ```routes.py``` associate handler functions with a template. For example, the ```about()``` function has an ```@view('about')``` decorator, so the dictionary it returns is rendered by the ```about.tpl``` template.

## /static folder

The ```static``` folder contains static assets used by the app, and has subfolders for CSS files, fonts, image files, and JavaScript scripts. Note that Bootstrap and JQuery are included.

## /docs folder

All of the documentation content. This page, for example.
