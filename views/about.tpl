% rebase('layout.tpl', title='About')
% import os
% import sys
% from about import sysinfo
% from routes import msgraphapi
% sysdict = sysinfo()
% free = int(sysdict['DISK_FREE'].replace(',', ''))
% total = int(sysdict['DISK_SIZE'].replace(',', ''))
% free_space = '{0} bytes ({1}% of total)'. \
%     format(sysdict['DISK_FREE'], int(100*free/total))

<h2>About</h2>

<h3>Auth Status</h3>

% if msgraphapi.loggedin:
  <table class="sysinfo">
  <tr><th>Authenticated&nbsp;identity:</th><td>{{ msgraphapi.loggedin_public }}</td></tr>
  <tr><th>User ID:</th><td>{{ msgraphapi.loggedin_id }}</td></tr>
  <tr><th>Access token:</th><td>{{ msgraphapi.token_abbrev(type='access') }}</td></tr>
  <tr><th>Refresh token:</th><td>{{ msgraphapi.token_abbrev(type='refresh') }}</td></tr>
  <tr><th>Scopes:</th><td>{{ ' / '.join(msgraphapi.token_scope.split(' ')) }}</td></tr>
  <tr><th>Token expires:</th><td>{{ '{0:.0f} seconds from now'.format(msgraphapi.token_seconds()) }}</td></tr>

  % if msgraphapi.loggedin_photo:
    <tr><th>Profile photo:</th><td><img src="data:image/png;base64,{{ msgraphapi.loggedin_photo }}" height="100" width="100"></td></tr>
  % end

  </table>
  <button type="button" class="btn btn-primary btn-md" onclick="window.location.href='/logout?redirect=/about'">Disconnect</button>
% else:
  <p>Not currently authenticated.</p>
  <button type="button" class="btn btn-primary btn-md" onclick="window.location.href='/login?redirect=/about'">Connect</button>
% end

<h3>System Information</h3>

<table class="sysinfo">
  <tr><th>OS version:</th>
    <td>{{ sysdict['OS_VERSION'] }}</td></tr>
  <tr><th>Host&nbsp;machine&nbsp;name:</th>
    <td>{{ sysdict['HOST_NAME'] }}</td></tr>
  <tr><th>Processor:</th>
    <td>{{ sysdict['HOST_PROC'] }}</td></tr>
  <tr><th>Server IP address:</th>
    <td>{{ sysdict['HOST_IPADDR'] }}</td></tr>
  <tr><th>Client IP address:</th>
    <td>{{ client_ip }}</td></tr>
   <tr><th>Working directory:</th>
    <td>{{ sysdict['DIRECTORY'] }}</td></tr>
  <tr><th>Free disk space:</th>
    <td>{{! free_space }}</td></tr>
</table>

<h3>Python Environment</h3>

<table class="sysinfo">
  <tr><th valign="top">Python version:</th>
    <td>{{ sysdict['PY_VERSION'] }}</td></tr>
  <tr><th>Virtual&nbsp;environment:</th>
    <td>{{ os.path.basename(sys.base_prefix) }}</td></tr>
  <tr><th>Python location:</th>
    <td>{{ sysdict['PY_LOCATION'] }}</td></tr>
</table>
