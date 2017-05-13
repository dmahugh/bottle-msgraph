% from routes import msgraphapi

% rebase('layout.tpl', title='home')

<div class="container homepage-container">

  <h2>bottle-msgraph</h2>

  % if msgraphapi.loggedin:
    <p class="ms-font-xl">Click the buttons below to see examples of working with the Graph API.</p>

    <table class = "api-endpoints">
      <tr>
        <th>Description</th>
        <th>Scope Required</th>
        <th>Graph API endpoint</th>
        <th></th>
      </tr>
      <tr>
        <td>Send Email</td>
        <td>Mail.Send</td>
        <td class="endpoint">/me/microsoft.graph.sendMail</td>
        <td style="padding-right: 25px"><button type="button" class="btn btn-block btn-primary btn-lg homepage" onclick="window.location.href='/sendmail'">Send email</button></td>
      </tr>
      <tr>
        <td>Inbox</td>
        <td>Mail.Read</td>
        <td class="endpoint">/me/mailFolders/Inbox/messages</td>
        <td style="padding-right: 25px"><button type="button" class="btn btn-block btn-primary btn-lg homepage" onclick="window.location.href='/inbox'">View inbox</button></td>
      </tr>
      <tr>
        <td>Contacts</td>
        <td>Contacts.Read</td>
        <td class="endpoint">/me/contacts</td>
        <td style="padding-right: 25px"><button type="button" class="btn btn-block btn-primary btn-lg homepage" onclick="window.location.href='/contacts'">View contacts</button></td>
      </tr>
      <tr>
        <td>Org Info</td>
        <td>User.Read</td>
        <td class="endpoint">/organization</td>
        <td style="padding-right: 25px"><button type="button" class="btn btn-block btn-primary btn-lg homepage" onclick="window.location.href='/orginfo'">Organization info</button></td>
      </tr>
    </table>

    <p>This is a Python Bottle app that demonstrates how to work with the <a href="https://graph.microsoft.io">Microsoft Graph API</a>. Source code and additional information can be found here: <a href="https://github.com/dmahugh/bottle-msgraph">https://github.com/dmahugh/bottle-msgraph</a></p>

  % else:
    <p>This is a Python Bottle app that demonstrates how to work with the <a href="https://graph.microsoft.io">Microsoft Graph API</a>. Source code and additional information can be found here: <a href="https://github.com/dmahugh/bottle-msgraph">https://github.com/dmahugh/bottle-msgraph</a></p>

    <p>To get started, click the button below to authenticate and give the app permissions, or select  one of the options from the menu above.</p>
    <button type="button" class="btn btn-primary btn-lg" onclick="window.location.href='/login'">Connect</button>
  % end
</div>
