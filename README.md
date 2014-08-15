fancyhands-python
=========

Python library for the [Fancy Hands API](https://www.fancyhands.com/developer). 
[Full documentation for the API](https://github.com/fancyhands/api/wiki) lives on github.

Version
----

0.1

Requirements
-----------
* [python-oauth2](https://github.com/simplegeo/python-oauth2)

Installation
--------------

Just copy the fancyhands-python/fancyhands directory to your project or:

```shell
git clone https://github.com/fancyhands/fancyhands-python
cd fancyhands-python
python setup.py install
```

Usage
----------
##### Dealing with 'custom' requests

```from fancyhands import FancyhandsClient

api_key = 'your_api_key'
secret = 'your_api_secret'

client = FancyhandsClient(api_key, secret)

# Get last 20 requests
requests = client.custom_get()

# Create a new request
from datetime import datetime, timedelta

title = 'Call Nicholas'
description = 'Tell him to make me some toast.'
bid = 4.0
expiration_date = datetime.now() + timedelta(1)

custom_fields = []
custom_field = {
  'label':'Response',
	'type':'textarea',
	'description':'When will my toast be done?',
	'order':1,
	'required':True,
}
custom_fields.append(custom_field)

request = client.custom_create(title, description, bid, expiration_date, custom_fields)
```

License
-------

[MIT](https://github.com/fancyhands/fancyhands-python/blob/master/LICENSE.txt)
