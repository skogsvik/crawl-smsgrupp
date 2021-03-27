# Message crawler for SMSgrupp.se

Crawl the entire history of a conversation on smsgrupp.se and store as a JSON document.

## Installation and Usage

To install required libraries, use pipenv:
```
pipenv update
```

To crawl a given conversation set the environment variables
* SMSGRUPP_TOKEN: The authentication token for api calls. Grab it simply by:
    1. Login to smsgrupp.se
    2. Open the network inspector
    3. Check the request headers of one of the GET calls to api.getsupertext.com
    4. Copy it from the `Auth-Token` field
* SMSGRUPP_GROUP_ID: The group id of the group to crawl. Get it simply by:
    1. Login to smsgrupp.se
    2. Open the target conversation
    3. Copy it from the URL on the form `https://www.smsgrupp.se/grupp/sapp/GROUP_ID`

The easiest way to set the environment variables is to create a `.env` file in the directory and set them there.

To finally run the crawler simply use pipenv again:
```
pipenv run crawler.py
```
