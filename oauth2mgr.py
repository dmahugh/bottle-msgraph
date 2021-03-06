"""OAuth2Manager class definition.
Copyright 2017 by Doug Mahugh. All Rights Reserved.
Licensed under the MIT License."""

import json
import os
import pprint
import time
import urllib.parse
import uuid

from bottle import redirect, request
import requests

class OAuth2Manager(object): #-----------------------------------------------<<<
    """Handles the details of obtaining an authorization code and access token
    from Azure Active Directory, and provides wrappers for making authenticated
    calls to the Microsoft Graph API.
    """
    def __init__(self, config=None):
        """The config argument is a dictionary of configuration settings. If it
        contains a configfile entry, settings are loaded from that file (a JSON
        dictionary), and then any other entries in the config dictionary are
        applied afterward (and can therefore override settings from the file).

        The config object may include any of these keys:
        configfile = name of JSON configuration file
        app_name = application name (as registered in an Azure AD tenant)
        app_id = application id (as registered in an Azure AD tenant)
        app_secret = application secret (as registered in an Azure AD tenant)
        redirect_url = redirect url (as registered in an Azure AD tenant)
        scopes = list of scopes needed (e.g., ['Mail.Send'])
        api_base = base URL for the protected resource/API; used for resolving
                   any relative URLs passed to the get() method
        auth_base = base URL for the authorization request
        token_url = URL for retrieving an access token via a POST
        """

        # initialize properties used for OAuth2 configuration ...
        self.app_name = ''
        self.app_id = ''
        self.app_secret = ''
        self.redirect_url = ''
        self.scopes = []
        self.api_base = ''
        self.auth_base = ''
        self.token_url = ''

        if 'configfile' in config:
            # Configuration filename provided, so merge those settings with
            # other settings (if any) in the config object. Note that any
            # explicit settings in the config object take precedence over
            #  settings from the configfile.
            filesettings = json.loads(open(config['configfile']).read())
            for key in filesettings:
                if key not in config:
                    config[key] = filesettings[key]

        # store configuration settings from config object
        if 'app_name' in config:
            self.app_name = config['app_name']
        if 'app_id' in config:
            self.app_id = config['app_id']
        if 'app_secret' in config:
            self.app_secret = config['app_secret']
        if 'redirect_url' in config:
            self.redirect_url = config['redirect_url']
        if 'scopes' in config:
            self.scopes = config['scopes']
        if 'api_base' in config:
            self.api_base = config['api_base']
        if 'auth_base' in config:
            self.auth_base = config['auth_base']
        if 'token_url' in config:
            self.token_url = config['token_url']

        # initialize properties used for caching session state ...
        self.auth_url = ''
        self.authcode = ''
        self.state = ''
        self.access_token = None
        self.token_type = ''
        self.token_expires_at = 0
        self.token_scope = ''
        self.refresh_token = None
        self.loggedin = False
        self.loggedin_id = ''
        self.loggedin_name = ''
        self.loggedin_email = ''
        self.loggedin_public = ''
        self.loggedin_photo = None
        self.cache('read') # read cached state (if any)

        # default is redirect to home page after login
        self.after_login = '/'

        if self.token_seconds() > 5:
            print('>>> OAuth2Manager: ' + \
                'cached access token is still valid for {0} seconds'. \
                format(self.token_seconds()))
        else:
            print('>>> OAuth2Manager: cached access token has expired')
            self.refresh_access_token()
            self.cache('save')

    def api_endpoint(self, url): #-------------------------------------------<<<
        """Convert a partial/relative endpoint to a full URL."""
        if url.split('/')[0].lower() in ['http:', 'https:']:
            return url
        else:
            return urllib.parse.urljoin(self.api_base, url.lstrip('/'))

    def authcode_abbrev(self, authcode=None):
        """Return an abbreviated version of an authorization code, for
        reporting purposes. Defaults to self.authcode if no authcode passed.
        """
        if not authcode:
            code = self.authcode
        if not code:
            return 'None'
        return code[:3] + '...' + code[-3:] + ' ({0} bytes)'.format(len(code))

    def authorized(self): #--------------------------------------------------<<<
        """We've been given an authorization code, so use it to request an
        access token."""

        # verify state received is same as state sent with the HTTPS request,
        # which confirms that we initiated this login attempt
        if self.state != request.query.state:
            raise Exception('>>> SHUTTING DOWN: state mismatch' + \
                '\n\nState SENT: {0}\n\nState RECEIVED: {1}'. \
                format(str(self.state), str(request.query.state)))
        self.state = '' # reset session state to prevent re-use

        token_response = self.fetch_token(request.query.code)
        if not token_response:
            print('>>> OAuth2Manager: request for access token failed')
            redirect('/')

        if not token_response.ok:
            # error - return to user the error text from Azure AD
            return token_response.text

        me_response = self.get('me')
        me_data = me_response.json()
        if 'error' in me_data:
            print('>>> OAuth2Manager: /me endpoint returned an error ... ' + \
                str(me_data))

        # set properties for current user name, email, public name (with domain)
        fullname = me_data['displayName']
        email = me_data['userPrincipalName']
        self.loggedin_id = me_data['id']
        self.loggedin_name = fullname
        self.loggedin_email = email
        if '@' in email:
            self.loggedin_public = '{0} (@{1})'. \
                format(fullname, email.split('@')[1].split('.')[0])
        else:
            self.loggedin_public = '{0} ({1})'.format(fullname, email)

        # save profile photo
        profile_pic = self.get('me/photo/$value', stream=True)
        if profile_pic.ok:
            import base64
            self.loggedin_photo = base64.b64encode(profile_pic.raw.read())
        else:
            self.loggedin_photo = None

        self.cache('save') # update cached auth state

        return redirect(self.after_login)

    def cache(self, action): #-----------------------------------------------<<<
        """Manage local cache for auth status.

        Three actions are supported:
        'save' = save current auth status
        'read' = restore auth status from cached version
        'clear' = clear the cached auth status
        """
        cachefile = 'cache.json'
        photofile = 'cache.photo'

        if action == 'save':
            configdata = dict(auth_url=self.auth_url,
                              access_token=self.access_token,
                              token_expires_at=self.token_expires_at,
                              token_scope=self.token_scope,
                              refresh_token=self.refresh_token,
                              loggedin=self.loggedin,
                              loggedin_id=self.loggedin_id,
                              loggedin_name=self.loggedin_name,
                              loggedin_email=self.loggedin_email,
                              loggedin_public=self.loggedin_public)
            open(cachefile, 'w').write(json.dumps(configdata))
            if os.path.isfile(photofile):
                os.remove(photofile) # clear any existing cached photo
            if self.loggedin_photo:
                open(photofile, 'wb').write(self.loggedin_photo)
        elif action == 'read':
            if os.path.isfile(cachefile):
                configdata = json.loads(open(cachefile).read())
                self.auth_url = configdata['auth_url']
                self.access_token = configdata['access_token']
                self.token_expires_at = configdata['token_expires_at']
                self.token_scope = configdata['token_scope']
                self.refresh_token = configdata['refresh_token']
                self.loggedin = configdata['loggedin']
                self.loggedin_id = configdata['loggedin_id']
                self.loggedin_name = configdata['loggedin_name']
                self.loggedin_email = configdata['loggedin_email']
                self.loggedin_public = configdata['loggedin_public']
                if os.path.isfile(photofile):
                    self.loggedin_photo = open(photofile, 'rb').read()
        else:
            # note that invalid actions will just clear the cache
            if os.path.isfile(cachefile):
                os.remove(cachefile)
            if os.path.isfile(photofile):
                os.remove(photofile)
            print('>>> OAuth2Manager: local cache cleared')

    def default_headers(self): #---------------------------------------------<<<
        """Returns the default HTTP headers for calls to the Graph API,
        including current access token.
        """

        # Note that we include a unique client-request-id HTTP header, which
        # is round-tripped by the Graph API and can be used to correlate a
        # request with its response for diagnostic purposes.
        return {'User-Agent' : 'bottle-msgraph/1.0',
                'Authorization' : 'Bearer {0}'.format(self.access_token),
                'Accept' : 'application/json',
                'Content-Type' : 'application/json',
                'client-request-id' : str(uuid.uuid4()),
                'return-client-request-id' : 'true'}

    def fetch_token(self, authcode): #---------------------------------------<<<
        """Get an OAuth2 access token. Requires the authorization code returned
        from auth_url."""
        self.authcode = authcode
        response = requests.post(self.token_url, \
            data=dict(client_id=self.app_id,
                      client_secret=self.app_secret,
                      grant_type='authorization_code',
                      code=authcode,
                      redirect_uri=self.redirect_url))
        if self.save_token(response):
            return response
        else:
            return None # the request for an access token failed

    def get(self, endpoint, headers=None, stream=False): #-------------------<<<
        """GET from API (authenticated with access token)."""
        # refresh token if within 5 seconds of expiring
        if self.token_seconds() < 5:
            self.refresh_access_token()

        merged_headers = self.default_headers()
        if headers:
            merged_headers.update(headers)
        return requests.get(self.api_endpoint(endpoint),
                            headers=merged_headers,
                            stream=stream)

    def login(self, redirect_to): #------------------------------------------<<<
        """Log in (authenticate against Azure AD)"""

        # create the "state"" GUID, which will be round-tripped by the auth_url
        # endpoint to verify that we initiated this login
        self.state = str(uuid.uuid4())

        # set url to redirect to after login completed
        self.after_login = redirect_to

        #Set the auth_url property, including all required OAuth2 parameters
        self.auth_url = self.auth_base + \
            ('' if self.auth_base.endswith('/') else '/') + \
            '?response_type=code&client_id=' + self.app_id + \
            '&redirect_uri=' + self.redirect_url + \
            '&scope=' + '%20'.join(self.scopes) + \
            '&state=' + self.state

        print('>>> OAuth2Manager: ask user to authenticate')
        redirect(self.auth_url, 302)

    def logout(self, redirect_to='/'): #-------------------------------------<<<
        """Log out of current connection and redirect to specified route.

        If redirect_to == None, no redirection will take place and we just
        clear the current logged-in status.
        """
        self.loggedin = False
        self.loggedin_name = ''
        self.loggedin_email = ''
        self.state = None
        self.access_token = None
        self.token_expires_at = 0
        self.cache('clear') # clear cached auth state

        if redirect_to:
            print('>>> OAuth2Manager: user logout')
            redirect(redirect_to)

    def post(self, endpoint, headers=None, data=None, verify=False, params=None):
        """POST to API (authenticated with access token).

        headers = custom HTTP headers (merged with defaults, including access token)

        verify = the Requests option for verifying SSL certificate; defaults
                 to False for demo purposes. For more information see:
        http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification
        """
        # refresh token if within 5 seconds of expiring
        if self.token_seconds() < 5:
            self.refresh_access_token()

        merged_headers = self.default_headers()
        if headers:
            merged_headers.update(headers)

        return requests.post(self.api_endpoint(endpoint),
                             headers=merged_headers, data=data,
                             verify=verify, params=params)

    def print_settings(self): #----------------------------------------------<<<
        """Print current property values to console."""
        print('>>> OAuth2Manager properties ...')
        pprint.pprint(self.__dict__)

    def refresh_access_token(self): #----------------------------------------<<<
        """Refresh the current access token."""
        response = requests.post(self.token_url, \
            data=dict(client_id=self.app_id,
                      client_secret=self.app_secret,
                      grant_type='refresh_token',
                      refresh_token=self.refresh_token))
        self.save_token(response)

    def save_token(self, response): #----------------------------------------<<<
        """Save an access token and related metadata.

        Input is the response object returned by the self.token_url endpoint.

        Returns True if the token was successfully saved, False if not. (For
        example, the token_url API may have returned no token.)
        """
        jsondata = response.json()
        if not 'access_token' in jsondata:
            self.logout(redirect_to=None) # log out and clear local cache
            print('>>> Oauth2Manager: request for access token failed')
            return False # no access token found

        self.access_token = jsondata['access_token']
        self.loggedin = True # we're authenticated now

        self.token_type = jsondata['token_type']
        if self.token_type != 'Bearer':
            print('>>> OAuth2Manager: expected Bearer token type, but received {0}'. \
                format(self.token_type))

        # Verify that the scopes returned include all scopes requested. The
        # offline_access scope is never returned by Azure AD, so we don't
        # include it in scopes_expected if present.
        scopes_expected = set([_.lower() for _ in self.scopes
                               if _.lower() != 'offline_access'])
        scopes_returned = \
            set([_.lower() for _ in jsondata['scope'].split(' ')])
        if scopes_expected > scopes_returned:
            print('WARNING: expected scopes not returned = {1}'. \
                format(' '.join(scopes_expected - scopes_returned)))
        self.token_scope = jsondata['scope']

        # token_expires_at = time.time() value (seconds) at which it expires
        self.token_expires_at = time.time() + int(jsondata['expires_in'])
        self.refresh_token = jsondata.get('refresh_token', None)

        print('>>> OAuth2Manager: access token acquired ({0} bytes)'. \
            format(len(self.access_token)))
        return True

    def token_abbrev(self, token_val=None, token_type='access'): #-----------<<<
        """Return abbreviated version of an access token for display purposes.

        If a token_val is provided, that value is is abbreviated.

        If no token_val is provided, the type argument determines the value:
        type == 'access' (default) - self.access_token
        type == 'refresh' - self.refresh_token
        """
        if not token_val:
            if token_type.lower() == 'refresh':
                token = self.refresh_token
            else:
                token = self.access_token
        if not token:
            return 'None'
        return token[:3] + '...' + token[-3:] + ' ({0} bytes)'.format(len(token))

    def token_seconds(self): #-----------------------------------------------<<<
        """Return integer (rounded) number of seconds before the current access
        token will expire, or 0 if already expired or no valid access token."""
        if not self.access_token or time.time() >= self.token_expires_at:
            return 0
        return round(self.token_expires_at - time.time())
