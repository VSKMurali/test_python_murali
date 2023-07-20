import requests
import json

# Calling API
response_API = requests.get('https://api.publicapis.org/entries')

# Printing status request of the API calls
print(response_API.status_code)

if response_API.status_code!=200:
    print("connection isn't successfull")
else:
    data = response_API.text
    parse_json = json.loads(data)

    count = parse_json['count']
    print("Count:",count)

    print(len(parse_json['entries']))

    for entries_list in parse_json['entries']:
        print (entries_list["API"])