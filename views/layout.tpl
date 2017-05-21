% from datetime import datetime
% from routes import msgraphapi

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - bottle-msgraph</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/site.css?version=1.01" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
            <span class="glyphicon glyphicon-menu-hamburger">
          </button>
          <a class="navbar-brand" href="/">Graph API Demo</a>
        </div>

        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li><a href="/sendmail"><span class="glyphicon glyphicon-send" aria-hidden="true"></span> Send Email</a></li>
            <li><a href="/inbox"><span class="glyphicon glyphicon-inbox" aria-hidden="true"></span> Inbox</a></li>
            <li><a href="/contacts"><span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span> Contacts</a></li>
            <li><a href="/orginfo"><span class="glyphicon glyphicon-briefcase" aria-hidden="true"></span> Org Info</a></li>
            <li><a href="/about"><span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> About</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            % if msgraphapi.loggedin:
              % if msgraphapi.loggedin_photo:
                <li class="profile-photo-hdr"><a href="/about"><img src="data:image/png;base64,{{ msgraphapi.loggedin_photo }}" height="16" width="16"> {{ msgraphapi.loggedin_public }}</a></li>
              % else:
                <li><a href="/about"><span class="glyphicon glyphicon-user"></span> {{ msgraphapi.loggedin_public }}</a></li>
              % end
            <li><a href="/logout?redirect=/"><span class="glyphicon glyphicon-log-out" aria-hidden="true"></span> Logout</a></li>
            % else:
            <li><a href="/login"><span class="glyphicon glyphicon-log-in" aria-hidden="true"></span> Login</a></li>
            % end
          </ul>
        </div>
      </div>
    </nav>

    <div class="container body-content">
        {{!base}}
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>

</html>
