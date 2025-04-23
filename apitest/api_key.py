import requests
import json

headers = {
  'Accept': 'application/json',
  'x-api-key': '$2a$10$yV57LdJMu9diLbCcqbOhLu8qqpgD68t.HxcbjNWJKdjphl.quxMky'
}

r = requests.get('https://api.curseforge.com/v1/categories',params={
  'gameId': '432'
}, headers = headers)

with open('curseforge_api_mod.json', 'w') as f:
    json.dump(r.json(), f)

# jsonpath='.\curseforge_api_key.json'

# with open(jsonpath,'r') as f:
#     data=json.load(f)
#     print(data)
