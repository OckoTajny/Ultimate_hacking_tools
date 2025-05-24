import requests

url = "http://51.20.104.53:8080/flag3"
cookies = {
    "TOKEN": "valid"
}

response = requests.get(url, cookies=cookies)

print("Status code:", response.status_code)
print("Tělo odpovědi:")
print(response.text)