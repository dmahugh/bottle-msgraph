% from routes import msgraphapi

% rebase('layout.tpl', title='contacts')

<div class="container">

  <h2>Contacts</h2>

  % if msgraphapi.loggedin:
    <p>First 10 contacts for {{ msgraphapi.loggedin_public }}, retrieved using the Microsoft Graph API.</p>
  % else:
    <p>To get started, click the button below and authenticate under one of your identities.</p>
    <button type="button" class="btn btn-primary btn-lg" onclick="window.location.href='/login?redirect=/inbox'">Connect</button>
  % end

</div>

% if msgraphapi.loggedin:
  % if status_code == 200:
    <table class="data-table">
      <tr>
        <th>Name</th>
        <th>Job Title</th>
        <th>Company Name</th>
        <th>Email</th>
      </tr>
      % for item in data:
        % emails = item['emailAddresses']
        % if emails:
          % email_str = ', '.join([_['address'] for _ in emails])
        % else:
          % email_str = ''
        % end
        <tr>
          <td>{{ item['displayName'] }}</td>
          <td>{{ item['jobTitle'] }}</td>
          <td>{{ item['companyName'] }}</td>
          <td>{{ email_str }}</td>
        </tr>
      % end
    </table>

    % http_color = ('green' if str(status_code).startswith('2') else 'red') if status_code else 'none'

    <table class = "api-endpoints" style="width: auto">
      <tr>
        <th>Scope Required</th>
        <th>Graph API endpoint</th>
        <th style="background: {{ http_color }};">HTTP Status</th>
      </tr>
      <tr>
        <td>Contacts.Read</td>
        <td class="endpoint">/me/contacts</td>
        <td style="text-align: center; color: white; background: {{ http_color }}">{{ status_code }}</td>
      </tr>
    </table>

  % else:
    <p>HTTP status code: {{ status_code }}</p>
  % end
% end
