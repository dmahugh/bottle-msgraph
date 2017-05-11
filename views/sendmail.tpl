% from routes import msgraphapi

% rebase('layout.tpl', title='sendmail')

<div class="container">

  <h2>Send Email</h2>

  % if not msgraphapi.loggedin:
    <p class="ms-font-xl">To get started, click the button below and authenticate under one of your identities.</p>
    <button type="button" class="btn btn-primary btn-lg" onclick="window.location.href='/login?redirect=/sendmail'">Connect</button>
  % end

  % if msgraphapi.loggedin:

    <div class="container" style="margin-top: 20px">

      <form action="/sendmail_action">
        <div class="form-group row">
          <label for="from" class="col-sm-1 col-form-label">From:</label>
          <div class="col-sm-4">
            <input type="email" class="form-control" id="from" name="from" value="{{ email }}" readonly>
          </div>
          <div class="col-sm-7">
            <button type="submit" class="btn btn-primary">Send Email</button>
          </div>
        </div>
        <div class="form-group row">
          <label for="email" class="col-sm-1 col-form-label">To:</label>
          <div class="col-sm-11">
            <input type="email" class="form-control" id="to" name="to" value="{{ email }}" autofocus style="min-width: 100%">
          </div>
        </div>
        <div class="form-group row">
          <label for="subject" class="col-sm-1 col-form-label">Subject:</label>
          <div class="col-sm-11">
            <input type="text" class="form-control" id="subject" name="subject" value="Hello from the Microsoft Graph API!" style="min-width: 100%">
          </div>
        </div>
        <div class="form-group row">
          <label for="body" class="col-sm-1 col-form-label">Body:</label>
          <div class="col-sm-11">
            <textarea class="form-control" id="body" name="body" cols="40" rows="5" style="min-width: 100%">This message was sent from a demo app using the Microsoft Graph API.</textarea>
          </div>
        </div>
      </form>
    </div>

    % if status_code:
      % if status_code == 200:
      <p class="ms-font-sm-green">Successfully sent email to {{ email }}! (status=200)</p>
      % elif status_code == 202:
      <p class="ms-font-sm-green">Email to {{ email }} accepted (status=202)</p>
      % else:
      <p class="ms-font-sm-red">Couldn't send email to {{ email }} (status={{ status_code }})</p>
      % end
    % end

    <table class = "api-endpoints" style="width: auto">
      <tr>
        <th>Scope Required</th>
        <th>Graph API endpoint</th>
      </tr>
      <tr>
        <td>Mail.Send</td>
        <td class="endpoint">/me/microsoft.graph.sendMail</td>
      </tr>
    </table>

  % end

</div>
