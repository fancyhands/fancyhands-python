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
pip install fancyhands
```
or

```shell
git clone https://github.com/fancyhands/fancyhands-python
cd fancyhands-python
python setup.py install
```

Usage
----------
##### Dealing with 'custom' requests

```python
from fancyhands import FancyhandsClient

api_key = 'your_api_key'
secret = 'your_api_secret'

client = FancyhandsClient(api_key, secret)

# Get last 20 requests
requests = client.custom_get()

# Create a new custom request
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

# Create a new standard request
title = "Call Ted"
description = "Tell him his toast is ready"

request = client.standard_create(title=title, description=description, bid=bid, expiration_date=expiration_date)

# Get a standard request
request = client.standard_get(key=request['key'])

# Message a standard request
client.standard_message(key=request['key'], message="Is the toast done yet")

# Create a new call request
# Visit: https://www.fancyhands.com/api/explorer/script/builder#/start
# Create a script for the assistant and paste it into your code
import json
conversation = json.dumps({"id":"sample_conversation","data":{},"name":"Sample Conversation","version":1.1,"scripts":[{"id":"start","steps":[{"name":"hello","type":"logic_control","note":"","prompt":"Hello, my name is $assistant_name","options":[{"name":"Continue","result":"sample_script"}]}]},{"id":"sample_script","steps":[{"name":"name","prompt":"What is your name?","type":"text","options":[]},{"name":"quest","prompt":"What is your quest?","type":"textarea","options":[]},{"type":"logic_control","name":"favorite_color","note":"","options":[{"name":"Red","result":"finish"},{"name":"Yellooooooooooooow","result":"finish","new_script":""},{"name":"Blue","result":"transfer"}],"prompt":"What is your favorite color?"}]},{"id":"finish","steps":[{"type":"logic_control","name":"goodbye","note":"","prompt":"Thank you $sample_script.name. I wish you good luck with $sample_script.quest.","options":[]}]},{"id":"transfer","steps":[{"type":"logic_control","name":"transfer","note":"","prompt":"$sample_script.favorite_color!!!? I wasn't expecting that... Please hold while I transfer you to my manager.","options":[{"name":"Transfer Call","result":"-- Transfer Call --"}]}],"transfer_number":"5555555555"}]})

# Add a valid US phone number
phone = '5555555555'

# Should we retry the call? This is not required
retry = True

# Retry every two hours
retry_delay = 60 * 60 * 2

# How many times to retry the call
retry_limit = 3

request = client.call_create(phone=phone, conversation=conversation, retry=retry, retry_delay=retry_delay, retry_limit=retry_limit)


```

License
-------

[MIT](https://github.com/fancyhands/fancyhands-python/blob/master/LICENSE.txt)
