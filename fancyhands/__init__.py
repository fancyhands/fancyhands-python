from urllib import urlencode
from datetime import datetime
import oauth2 as oauth
import json

API_HOST = 'https://www.fancyhands.com'

class FancyhandsClient(object):
    ##########################################################################################
    # Utility
    ##########################################################################################
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret

    def oauth_request(self, uri='', query_params={}, http_method='GET'):
        url = API_HOST + uri

        consumer = oauth.Consumer(key=self.api_key, secret=self.secret)
        client = oauth.Client(consumer)

        if http_method == 'GET':
            url += '?%s' % urlencode(query_params)
            resp, content = client.request(url, http_method)
        elif http_method == 'POST':
            resp, content = client.request(url, http_method, body=urlencode(query_params))
        elif http_method == 'PUT':
            resp, content = client.request(url, http_method, body=urlencode(query_params), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        elif http_method == 'DELETE':
            url += '?%s' % urlencode(query_params)
            resp, content = client.request(url, http_method)

        try:
            content = json.loads(content)
        except:
            raise Exception(content)

        return content
 

    # just a simple echo request
    def echo_get(self, params={}):
        uri = '/api/v1/echo/'
        return self.oauth_request(uri=uri, query_params=params, http_method='GET')

    # just a simple echo request
    def echo_post(self, params={}):
        uri = '/api/v1/echo/'
        return self.oauth_request(uri=uri, query_params=params, http_method='POST')
    
    
    ##########################################################################################
    # Custom API
    ##########################################################################################

    # This will allow you to get any request you have submitted.
    def custom_get(self, key=None, status=None, cursor=None):
        uri = '/api/v1/request/custom/'

        query_params = {
            'key': key,
            'status': status,
            'cursor': cursor,
        }
        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')


    # This will allow you to submit a task, specify which data you'd like back (custom_fields) and set the price (bid) you're willing to pay.
    # (expiration_date) needs to be a python datetime and marks when the task will expire if not picked up by an assistant.
    def custom_create(self, title=None, description=None, bid=None, expiration_date=None, custom_fields={}, test=False):
        uri = '/api/v1/request/custom/'

        query_params = {
            'title': title,
            'description': description,
            'bid': bid,
            'expiration_date': expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'custom_fields': json.dumps(custom_fields),
            'test':test,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')

    # This is the cancel method. Calling this method will cancel a request from being completed. 
    # If the task hasn't been started, you can cancel. Otherwise, it will fail. 
    def custom_cancel(self, key=None):
        uri = '/api/v1/request/custom/cancel/'

        query_params = {
            'key': key,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')



    ##########################################################################################
    # Outgoing API
    ##########################################################################################

    # This will allow you to get any call request you have submitted.
    def outgoing_get(self, key=None, status=None, cursor=None):
        uri = '/api/v1/call/outgoing/'

        query_params = {
            'key': key,
            'status': status,
            'cursor': cursor,
        }
        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')


    
    # This will allow you to submit a call task. (phone) is the phone number to be called. (conversation) is the json encoded
    # script for the assistants.
    def outgoing_create(self, phone=None, conversation=None, title=None, record=False, retry=False, retry_delay=None,
                        retry_limit=None, call_window_start=None, call_window_end=None, test=False):
        uri = '/api/v1/call/outgoing/'

        query_params = {
            'phone': phone,
            'conversation': conversation,
            'record':record,
            'retry':retry,
            'retry_delay':retry_delay,
            'retry_limit':retry_limit,
            'title':title,
            'test':test,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        if call_window_start and call_window_end:
            query_params['call_window_start'] = call_window_start.strftime('%Y-%m-%dT%H:%M:%SZ')
            query_params['call_window_end'] = call_window_end.strftime('%Y-%m-%dT%H:%M:%SZ')

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')

    ##########################################################################################
    # Number API
    ##########################################################################################
    def number_buy(self, phone_number=None):
        uri = '/api/v1/call/number/'

        query_params = {
            'phone_number':phone_number,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')['phone_numbers']

    def number_get(self, area_code=None, contains=None, region=None):
        uri = '/api/v1/call/number/'

        query_params = {
            'area_code':area_code,
            'contains':contains,
            'region':region,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')['phone_numbers']

    def number_delete(self, phone_number=None, key=None):
        uri = '/api/v1/call/number/'

        query_params = {
            'phone_number':phone_number,
            'key':key,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='DELETE')

    ##########################################################################################
    # Incoming API
    ##########################################################################################
    def incoming_create(self, phone_number=None, conversation=None):
        uri = '/api/v1/call/incoming/'

        query_params = {
            'phone_number':phone_number,
            'conversation':conversation,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')['call']

    def incoming_get(self, key=None, phone_number=None, cursor=None):
        uri = '/api/v1/call/incoming/'

        query_params = {
            'key':key,
            'phone_number':phone_number,
            'cursor':cursor,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')

    def incoming_modify(self, key=None, phone_number=None, conversation=None):
        uri = '/api/v1/call/incoming/'

        query_params = {
            'key':key,
            'phone_number':phone_number,
            'conversation':conversation,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='PUT')

    def incoming_delete(self, phone_number=None, key=None):
        uri = '/api/v1/call/incoming/'

        query_params = {
            'key':key,
            'phone_number':phone_number,
        }

        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='DELETE')

    ##########################################################################################
    # History API
    ##########################################################################################
    # Todo - Test
    def history(self, key=None, phone_number=None, cursor=None):
        uri = '/api/v1/call/history/'

        query_params = {
            'key': key,
            'phone_number': phone_number,
            'cursor': cursor,
        }
        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')


    ##########################################################################################
    # Standard API
    ##########################################################################################

    def standard_get(self, key=None, status=None, cursor=None):
        uri = '/api/v1/request/standard/'

        query_params = {
            'key': key,
            'status': status,
            'cursor': cursor,
        }
        query_params = {i:j for i,j in query_params.items() if j != None}

        return self.oauth_request(uri=uri, query_params=query_params, http_method='GET')

    def standard_create(self, title=None, description=None, bid=None, expiration_date=None, test=False):
        uri = '/api/v1/request/standard/'

        query_params = {
            'title': title,
            'description': description,
            'bid': bid,
            'expiration_date': expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'test':test,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')

    ##########################################################################################
    # Messages API
    ##########################################################################################

    def standard_message(self, key=None, message=None):
        uri = '/api/v1/request/standard/messages/'

        query_params = {
            'key': key,
            'message': message,
        }

        return self.oauth_request(uri=uri, query_params=query_params, http_method='POST')
