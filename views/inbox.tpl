% from routes import msgraphapi

% rebase('layout.tpl', title='inbox')

<div class="container">

  <h2>Inbox</h2>

  % if msgraphapi.loggedin:
    <p>The 10 most recent items in the inbox of {{ msgraphapi.loggedin_public }}, retrieved using the Microsoft Graph API.</p>
  % else:
    <p>To get started, click the button below and authenticate under one of your identities.</p>
    <button type="button" class="btn btn-primary btn-lg" onclick="window.location.href='/login?redirect=/inbox'">Connect</button>
  % end

</div>

% if msgraphapi.loggedin:
  % if status_code == 200:
    <table class = "data-table">
      <tr>
        <th>Received</th>
        <th>From</th>
        <th>Subject</th>
      </tr>
      % for item in data:
        <tr>
          <td>{{ item['receivedDateTime'] }}</td>
          % from_name = item['from']['emailAddress']['name']
          % from_addr = item['from']['emailAddress']['address']
          <td>{{ '{0} ({1})'.format(from_name, from_addr) }}</td>
          <td>{{ item['subject'] }}</td>
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
        <td>Mail.Read</td>
        <td class="endpoint">/me/mailFolders/Inbox/messages</td>
        <td style="text-align: center; color: white; background: {{ http_color }}">{{ status_code }}</td>
      </tr>
    </table>

  % else:
    <p>HTTP status code: {{ status_code }}</p>
  % end
% end
