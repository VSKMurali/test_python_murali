import requests
import json

# API Name
response_API = 'https://httpbin.org/post'
# Headers
headers = {"Content-Type": "application/json; charset=utf-8"}
#Body (Pay load data) 
data = {
    "id": 1001,
    "name": "geek",
    "passion": "coding",
    "nation" : "india"
}
#Calling API server 
response = requests.post(response_API, headers=headers, json=data)

# Printing status request of the API call
print(response.status_code)

if response.status_code!=200:
    print("connection isn't successfull")
else:
    data = response.text
    print(data)

    parse_json = json.loads(data)

    origin = parse_json['origin']
    urlStr = parse_json['url']

    print("origin:",origin)
    print("urlStr:",urlStr)
    print("id:",parse_json['json']['id'])
    print("name",parse_json['json']['name'])
    print("passion",parse_json['json']['passion'])
    print("nation",parse_json['json']['nation'])