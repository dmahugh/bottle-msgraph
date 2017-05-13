# bottle-msgraph

Simple web app that shows how to connect to the [Microsoft Graph API](https://developer.microsoft.com/en-us/graph/) in Python. This sample does not use an SDK or auth provider, because it was created as an OAuth 2.0 learning exercise.

Authentication functionality is in the [OAuth2Manager](docs/OAuth2Manager) class defined in [oauth2mgr.py](https://github.com/dmahugh/bottle-msgraph/blob/master/oauth2mgr.py), and the methods of OAuth2Manager print console status messages to provide visibility into what's going on. Here's an example of app startup after a cached access token has expired:

![app startup screenshot](docs/images/appstartup.png)

For information about how to install and use the sample, see the documentation:

[Installation](docs/Installation) | [Getting Started](docs/GettingStarted) | [Overview](docs/Overview) | [Sample Queries](docs/SampleQueries) | [OAuth2Manager class](docs/OAuth2Manager)

Pull requests are welcome, or feel free to [log an issue](https://github.com/dmahugh/bottle-msgraph/issues)
if you have a suggestion or run into any issues. Thanks!

## Where to Learn More

* The [Microsoft Graph API](https://developer.microsoft.com/en-us/graph/) site has a variety of information for Graph developers, including SDKs for many languages, code samples, and documentation.
* The [Oauth 2.0 specification](http://www.rfc-editor.org/rfc/rfc6749.txt) is the official documentation for OAuth2 process flow details. As specs go, it's small (just 75 pages), well-organized, and easy to read. 
* For an overview of how to implement OAuth 2.0 authorization code flow for Azure Active Directory in web apps, see this page: [Authorize access to web applications using OAuth 2.0 and Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-protocols-oauth-code)
* The [Open ID Connect specifications](http://openid.net/connect/) are optional reading for most application developers, but it's worth noting that Azure AD only returns refresh tokens if the _offline_access_ scope is included in the requested scopes, as covered in [Section 11](http://openid.net/specs/openid-connect-core-1_0.html#OfflineAccess) of the Open ID Connect [core spec](http://openid.net/specs/openid-connect-core-1_0.html).
