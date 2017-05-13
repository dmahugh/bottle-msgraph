% from routes import msgraphapi

% rebase('layout.tpl', title='sendmail')

<div class="container">

  <h2>Send Email</h2>

  % if not msgraphapi.loggedin:
    <p>To get started, click the button below and authenticate under one of your identities.</p>
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

    % http_color = ('green' if str(status_code).startswith('2') else 'red') if status_code else 'none'

    <table class = "api-endpoints" style="width: auto">
      <tr>
        <th>Scope Required</th>
        <th>Graph API endpoint</th>
        % if status_code:
          <th style="background: {{ http_color }};">HTTP Status</th>
        % end
      </tr>
      <tr>
        <td>Mail.Send</td>
        <td class="endpoint">/me/microsoft.graph.sendMail</td>
        % if status_code:
          <td style="text-align: center; color: white; background: {{ http_color }}">{{ status_code }}</td>
        % end
      </tr>
    </table>

  % end

</div>
