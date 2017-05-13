"""Route handlers for bottle-msgraph sample app.
Copyright 2017 by Doug Mahugh. All Rights Reserved.
Licensed under the MIT License."""
import json
import os
import platform
import shutil
import socket
import sys
from pip.operations import freeze

from bottle import error, redirect, request, route, template, view
import oauth2mgr

msgraphapi = oauth2mgr.OAuth2Manager()

@route('/about')
@view('about')
def about(): #---------------------------------------------------------------<<<
    """About page - about.tpl"""
    sys_info = dict()
    sys_info['PY_VERSION'] = sys.version.strip().split(' ')[0] + \
        (' (64-bit)' if '64 bit' in sys.version else ' (32-bit)')
    sys_info['PY_LOCATION'] = sys.prefix
    sys_info['PY_PACKAGES'] = ','.join([_ for _ in freeze.freeze()])
    sys_info['PY_PATH'] = ','.join(sys.path)
    sys_info['OS_VERSION'] = platform.platform()
    sys_info['HOST_NAME'] = socket.gethostname()
    sys_info['HOST_PROC'] = \
        os.environ['PROCESSOR_ARCHITECTURE'] + ', ' + \
        os.environ['PROCESSOR_IDENTIFIER'].split(' ')[0] + ', ' + \
        os.environ['NUMBER_OF_PROCESSORS'] + ' cores'
    sys_info['HOST_IPADDR'] = socket.gethostbyname(socket.gethostname())
    sys_info['CLIENT_IP'] = request.environ.get('REMOTE_ADDR')
    sys_info['DIRECTORY'] = os.getcwd()
    size, used, free = shutil.disk_usage('/')
    sys_info['DISK_SIZE'] = '{:,}'.format(size)
    sys_info['DISK_USED'] = '{:,}'.format(used)
    sys_info['DISK_FREE'] = '{:,}'.format(free)
    return dict(sysdict=sys_info)

@route('/login/authorized')
def authorized(): #----------------------------------------------------------<<<
    """Handler for login/authorized route."""
    return msgraphapi.authorized()

@route('/clearcache')
def clearcache(): #----------------------------------------------------------<<<
    """Handler for /clearcache endpoint."""
    msgraphapi.cache('clear')
    redirect(request.query.redirect or '/')

@route('/contacts')
@view('contacts')
def contacts(): #------------------------------------------------------------<<<
    """Show current user's contacts."""
    if not msgraphapi.loggedin:
        return dict()

    response = msgraphapi.get('me/contacts')
    jsondata = response.json().get('value', None)
    nextpage_url = response.json().get('@odata.nextLink', None)
    return dict(status_code=response.status_code,
                data=jsondata,
                nextlink=nextpage_url)

@error(404)
@view('404error')
def custom404handler(err): #-------------------------------------------------<<<
    """Custom handler for 404 errors."""
    return dict(err=err)

@route('/')
@route('/home')
@view('index')
def home(): #----------------------------------------------------------------<<<
    """Renders the home page."""
    return dict()

@route('/inbox')
@view('inbox')
def inbox(): #---------------------------------------------------------------<<<
    """Show email inbox."""
    if not msgraphapi.loggedin:
        return dict()

    response = msgraphapi.get('me/mailFolders/Inbox/messages')
    jsondata = response.json().get('value', None)
    nextpage_url = response.json().get('@odata.nextLink', None)
    return dict(status_code=response.status_code,
                data=jsondata,
                nextlink=nextpage_url)

@route('/login')
def login(): #---------------------------------------------------------------<<<
    """Handler for /login endpoint."""
    msgraphapi.login(request.query.redirect or '/')

@route('/logout')
def logout(): #--------------------------------------------------------------<<<
    """Handler for /logout endpoint."""
    after_logout = request.query.redirect
    if not after_logout:
        after_logout = '/'
    msgraphapi.logout(after_logout)

@route('/orginfo')
@view('orginfo')
def orginfo(): #-------------------------------------------------------------<<<
    """Renders the organization info page."""
    if not msgraphapi.loggedin:
        return dict()

    response = msgraphapi.get('organization')
    if response.status_code == 200 and response.json()['value']:
        # current user is in an organization managed by Azure AD
        data = response.json()['value'][0]
        return dict(org_id=data['id'],
                    org_name=data['displayName'],
                    status_code=response.status_code,
                    errmsg='')
    else:
        # no 'value' returned, so current user is not in an organization
        return dict(org_id=None,
                    org_name=None,
                    status_code=response.status_code,
                    errmsg=response.text)

def print_env(title, req_obj=None, oauthmgr=None): #-------------------------<<<
    """Print route handler environment details (for debugging purposes).
    """
    if req_obj:
        print((' ' + title + ' - request object ').center(80, '-'))
        print('HTTP_ACCEPT:       {0}'.format(req_obj['HTTP_ACCEPT']))
        print('HTTP_USER_AGENT:   {0}'.format(req_obj['HTTP_USER_AGENT']))
        print('QUERY_STRING:      {0}'.format(req_obj['QUERY_STRING']))
        print('bottle.app.config: {0}'.format(req_obj['bottle.app'].config))
        print('bottle.raw_path:   {0}'.format(req_obj['bottle.raw_path']))
        print('bottle.request:    {0}'.format(req_obj['bottle.request']))
        print('bottle.route:      {0}'.format(req_obj['bottle.route']))
        print('route.handle:      {0}'.format(req_obj['route.handle']))
        print('route.url_args:    {0}'.format(req_obj['route.url_args']))
    if oauthmgr:
        print((' ' + title + ' - OAuth2Manager object ').center(80, '-'))
        print('api_base:          {0}'.format(oauthmgr.api_base))
        print('app_id:            {0}'.format(oauthmgr.app_id))
        print('app_name:          {0}'.format(oauthmgr.app_name))
        print('app_secret:        {0}'.format(oauthmgr.app_secret))
        print('auth_base:         {0}'.format(oauthmgr.auth_base))
        print('auth_url:          {0}'.format(oauthmgr.auth_url))
        print('authcode:          {0}'.format(oauthmgr.authcode_abbrev()))
        print('loggedin:          {0}'.format(oauthmgr.loggedin))
        print('loggedin_email:    {0}'.format(oauthmgr.loggedin_email))
        print('loggedin_name:     {0}'.format(oauthmgr.loggedin_name))
        print('redirect_url:      {0}'.format(oauthmgr.redirect_url))
        print('scopes:            {0}'.format(oauthmgr.scopes))
        print('state:             {0}'.format(oauthmgr.state))
        print('token_expires_at:  {0} ({1:.0f} seconds from now)'. \
            format(oauthmgr.token_expires_at, oauthmgr.token_seconds()))
        print('token_url:         {0}'.format(oauthmgr.token_url))
        print('access_token:      {0}'.format(oauthmgr.token_abbrev()))

@route('/sendmail')
@view('sendmail')
def sendmail(): #------------------------------------------------------------<<<
    """Handler for /sendmail route, the "send an email" page."""
    return dict(fullname=msgraphapi.loggedin_name,
                email=msgraphapi.loggedin_email,
                status_code=None)

@route('/sendmail_action')
def sendmail_action(): #-----------------------------------------------------<<<
    """Send an email to the address entered in the sendmail form."""

    if not msgraphapi.loggedin:
        redirect('/sendmail')

    email_body = json.dumps( \
        {'Message': {'Subject': request.query.subject,
                     'Body': {'ContentType': 'HTML', \
                     'Content': request.query.body},
                     'ToRecipients': [{'EmailAddress': {'Address': request.query.to}}]},
         'SaveToSentItems': 'true'})

    # send the email
    response = msgraphapi.post(endpoint='me/microsoft.graph.sendMail',
                               data=email_body)

    # refresh the sendmail page, showing result (status_code) for this action
    return template('sendmail.tpl',
                    dict(fullname=msgraphapi.loggedin_name,
                         email=msgraphapi.loggedin_email,
                         status_code=response.status_code))

@route('/refresh_token')
def token_refresh(): #-------------------------------------------------------<<<
    """Handler for refreshing access token."""
    msgraphapi.refresh_access_token()
    redirect(request.query.redirect_to)
