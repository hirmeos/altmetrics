Twitter API Limitations
=======================

At the present time (08 March 2019), we have run into a few limitation with
regard to using the Twitter's API (explained in Twitter's documentation). As a
result we have determined that the Altmetrics service will only be able to keep
track of recent tweets relating to books, and will be unable to fetch historical
tweet data from the Twitter API - we will rely solely on Crossref Event Data for
this.

This is due to the limitations described below.

The Standard API
----------------

This is Twitter's public API. It allows users to search for tweets that
happened up to 7 days ago. Obviously, this cannot be used to fetch historical
tweet data, but it is very useful to keep up to date with current tweets.

The Premium API
---------------

The Premium API supports a full-archive search, which allows users to find
tweets as far back as March of 2006.

It must be noted that users can only search for tweets that took place in
31-day windows - e.g. from 01 May 2017 until the 31 May 2017. This means that
if a book was published a year ago, it would require 12 different requests to
the API to search for any tweets about the book.

In addition to this, Twitter currently impose a limit of 50 requests per month
on this full-archive search. As a result, it is not feasible for us to use this
API to search for tweets about books.

General Rate limitations
------------------------

Twitter does apply limits to how often a user or app can make a request to the
API. This is done in 15-minute windows - see the link below for rate-limiting
of the Standard API.

It is important to check the HTTP Headers included in responses from the API
to check how many requests are allowed in the current window, as well as
when the current window is reset.

With the twittersearch python client the `get_metadata()` method can be used to
access the `x-rate-limit-remaining` and `x-rate-limit-reset` headers for this
purpose.



Useful links / references
-------------------------


**Overview of Twitter's API products**
https://developer.twitter.com/en/docs/tweets/search/overview

**Twitter rate-limiting on their standard API**
https://developer.twitter.com/en/docs/basics/rate-limiting.html

**Subscriptions - check the limitations available for different accounts**
(Only if you are logged in with a twitter dev account)
It may be useful to keep an eye on this in case these change.
https://developer.twitter.com/en/account/subscriptions

**twittersearch python client (PyPI)**
https://pypi.org/project/TwitterSearch
