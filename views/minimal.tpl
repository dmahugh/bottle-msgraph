% from minroutes import msgraphapi

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>graph-inbox</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/minimal.css?version=1.01" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="container homepage-container">

        <h2>Minimal OAuth2Manager Implementation in Bottle</h2>

        % if msgraphapi.loggedin:

            <table class="homepage">
                <tr>
                    <td><button type="button" class="btn btn-homepage btn-lg" onclick="window.location.href='/logout'">Disconnect</button></td>
                    <td>Current Identity: <strong>{{ msgraphapi.loggedin_public }}</strong></td>
                    <td>
                        % if msgraphapi.loggedin_photo:
                            <img class="profile-photo" src="data:image/png;base64,{{ msgraphapi.loggedin_photo }}">
                        % end
                    </td>
                </tr>
            </table>

            <table class = "inbox">
                <tr><th>Date</th><th>From</th><th>Subject</th></tr>
                % for item in data:
                <tr>
                    <td>{{ item['receivedDateTime'][:10] }}</td>
                    % from_name = item['from']['emailAddress']['name']
                    % from_addr = item['from']['emailAddress']['address']
                    <td>{{ '{0} ({1})'.format(from_name, from_addr)[:30] + ' ...' }}</td>
                    <td>{{ item['subject'][:30] + ' ...' }}</td>
                </tr>
                % end
            </table>

        % else:

            <table class="homepage">
                <tr>
                    <td><button type="button" class="btn btn-homepage btn-lg" onclick="window.location.href='/login'">Connect</button></td>
                    <td colspan=2>To get started, click the button below to authenticate and give the app permissions.</td>
                <tr>
            </table>

        % end

    </div>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>
