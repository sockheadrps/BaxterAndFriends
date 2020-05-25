import requests
import json


data = {"some": "data"}
url = 'http://localhost:8000/add_song'
r = requests.post(url=url,  data={"data": json.dumps(data)})
print(r.headers, r.content)
data = r.json()
print(data)