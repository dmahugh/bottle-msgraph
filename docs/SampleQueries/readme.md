# Sample Queries

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

The following sample queries are demonstrated in the app.

## Send Email

This example uses the Graph API's ```/me/microsoft.graph.sendMail``` endpoint to send an email on behalf of the current user. An HTML form is provided for entering the destination email, subject, and message body:

![sendmail](../images/sendmail.png)

## Inbox

This example uses the Graph API's ```/me/mailFolders/Inbox/messages``` to retrieve the 10 most recent emails from the user's email inbox:

![inbox](../images/inbox.jpg)

## Contacts

This example uses the Graph API's ```/me/contacts``` endpoint to retrieve the first 10 contacts for the current user:

![contacts](../images/contacts.jpg)

## Org Info

This example uses the Graph API's ```/organization``` endpoint to retrieve information about the current user's organization:

![orginfo](../images/orginfo.jpg)
