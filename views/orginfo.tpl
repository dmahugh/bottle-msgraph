% from routes import msgraphapi

% rebase('layout.tpl', title='org info')

<div class="container">

  <h2>Organization Info</h2>

  % if msgraphapi.loggedin:

    <p class="ms-font-xl">Information about the organization of {{ msgraphapi.loggedin_public }}, retrieved using the Microsoft Graph API.</p>

    <table class="orginfo">
      <tr><th>Authenticated Identity:</th><td>{{ msgraphapi.loggedin_public }}</td></tr>

      % if status_code == 200 and org_id:
        <tr><th>Organization ID:</th><td>{{ org_id }}</td></tr>
        <tr><th>Organization Name:</th><td>{{ org_name }}</td></tr>
      % else:
        <tr><th></th><td>This identity is not in an organization.</td></tr>
      % end

      % if status_code != 200:
        <tr><th>HTTP status code:</th><td>{{ status_code }}
        % if errmsg:
          <br/>{{ errmsg }}
        % end
        </td></tr>
      % end

    </table>

    <table class = "api-endpoints" style="width: auto">
      <tr>
        <th>Scope Required</th>
        <th>Graph API endpoint</th>
      </tr>
      <tr>
        <td>User.Read</td>
        <td class="endpoint">/organization</td>
      </tr>
    </table>

  % else:

    <p class="ms-font-xl">To get started, click the button below and authenticate under one of your identities.</p>
    <button type="button" class="btn btn-primary btn-lg" onclick="window.location.href='/login?redirect=/orginfo'">Connect</button>

  % end

</div>
