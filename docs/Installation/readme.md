# Installation

[Installation](../Installation/readme.md) | [Getting Started](../GettingStarted/readme.md) | [Overview](../Overview/readme.md) | [Sample Queries](../SampleQueries/readme.md) | [OAuth2Manager class](../OAuth2Manager/readme.md) | [repo home](https://github.com/dmahugh/bottle-msgraph)

This sample is intended as a Graph/AAD/OAuth2 learning tool for _Python_ developers, so the following instructions assume that you're familiar with installing Python packages and working with Python virtual environments.

Clone the https://github.com/dmahugh/bottle-msgraph repo to get the app, and then install these prerequisites:

* [Python 3.6](https://www.python.org/) (should_ work with any Python 3.x version, but I haven't tested others)
* [Bottle](https://bottlepy.org/docs/dev/) web micro-framework
* [Requests](http://docs.python-requests.org/en/master/) library for handling HTTP requests

Use of a virtual environment is recommended. If you're using [Conda](https://conda.io/docs/index.html) to manage virtual environments, note that Bottle isn't currently available as a Conda package so you'll need to install it with pip after you create the virtual environment:

```
conda create --name <envname> python=3.6 requests
activate <envname>
pip install bottle
```

After installing Python, Bottle, and Requests, you're ready to configure and run the sample app as covered in [Getting Started](../GettingStarted/readme.md).
