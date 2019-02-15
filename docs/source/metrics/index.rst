Altmetrics
==========

Setting up your user account
----------------------------

You can register for an account at https://altmetrics.ubiquity.press/register.

You will be sent a an email asking you to confirm the email address you
supplied. Click on the link given in this email.

To prevent unwanted traffic on the metrics API we will need to approve your
account before you can use the service. Once a site admin has approved your
account will receive an email letting you know that you may use the Altmetrics
service.


Using the API
-------------

Postman API Documentation
.........................

For those who are familiar with Postman, the Altmetrics API has been documented
using Postman, and a JSON copy of this documentation can be found at
https://github.com/hirmeos/altmetrics/tree/master/docs/postman.


Getting a token
...............

Most requests to the Altmetrics API will need to validated with a JSON Web Token
(JWT). The process of acquiring and using a JWT will be explained below.
**Please note: Your account will need to be approved before you can be issued
a JWT**.

**API endpoint:** https://altmetrics.ubiquity.press/api/get_token

**Method:** `GET`

Your request will need to be authenticated using basic authentication. This
will use your login details as `username`:`password`, where `username` is the
email you registered with and `password` is your password.

Example: Assuming a user registers with the following credentials
    - **email:** test.user@gmail.com
    - **password:** test-password-123

With `curl`, this can be done as either

    .. code-block:: bash

        curl -u test.user@gmail.com:test-password-123 https://altmetrics.ubiquity.press/api/get_token

or using the base64 encoding of `username`:`password`

    .. code-block:: bash

        curl --header "Authorization: Basic dGVzdC51c2VyQGdtYWlsLmNvbTp0ZXN0LXBhc3N3b3JkLTEyMw==" https://altmetrics.ubiquity.press/api/get_token


Token Bearer schema
...................

Once you have a token, all requests to the Altmetrics API will require you to
use this token to authenticate yourself. To do this, simply add the token to
your request header, as follows.

    .. code-block:: bash

        Authorization: Bearer [token]

Where `[token]` represents your JWT.


Registering DOIs
................

You can post the DOIs of works to the Altmetrics API.

**API endpoint:** https://altmetrics.ubiquity.press/api/uriset

**Method:** `POST`

**JSON format:** The Altmetrics API expects to receive JSON, containing a list
of DOIs in the format shown below. Each DOI can be registered with zero or more
URLs.

    .. code-block:: python

        [
            {
                "doi": DOI
                "url": [
                    URL1,
                    URL2,
                    URL3,
                ]
            }
        ]


Refer to postman JSON for an example call to this API endpoint.


Querying DOIs
.............

Check all DOIs associated with your user account. Remember to authenticate
yourself with your JWT.

**API endpoint:** https://altmetrics.ubiquity.press/api/uriset

**Method:** `GET`

Refer to postman JSON for an example call to this API endpoint.

