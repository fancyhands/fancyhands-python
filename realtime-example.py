from fancyhands import FancyhandsClient

api_key = ''
secret = ''

client = FancyhandsClient(api_key, secret)

response = client.realtime_request_create("Test task!")

if response.get('status') != 'ok':
    quit("Uh. oh")
    
req = response.get('request')
print req.get('status'), req.get('status_name')

client.realtime_message_create(req.get('key'), "This is my first message.")
client.realtime_message_create(req.get('key'), "This is my second message.")
client.realtime_message_create(req.get('key'), "This is my third message.")
client.realtime_message_create(req.get('key'), "You can just close this. Thanks!.")

messages = client.realtime_message_get(req.get('key'))

for x in messages.get('messages'):
    print x.get('type'), x.get('content')



