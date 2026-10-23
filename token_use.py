import requests

url = "https://api.deepseek.com/user/balance"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer sk-47ce4d004bba415d8b75a5592c883857'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)