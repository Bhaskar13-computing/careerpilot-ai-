import requests

url = "http://127.0.0.1:5000/get-roadmap"

data = {
    "branch": "CSE",
    "year": "1",
    "interest": "SoftwareDevelopment"
}

res = requests.post(url, json=data)
print(res.json())
