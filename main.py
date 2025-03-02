import requests

url = "https://esb-acc.level-level.nl/"
username = "levellevel"
password = "staging"

session = requests.Session()
session.auth = (username, password)
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

response = session.get(url)
print(response.status_code)
