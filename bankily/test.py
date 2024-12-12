import requests 
url = "https://ebankily-tst.appspot.com/authentification"
body ={
    "grant_type" : "password",
    "username" : "IMTIYAZ",
    "password" : "12345",
    "client_id" : "ebankily",
}
headers = {
    "Content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=body, headers=headers)

token = response.json().get('')

url = "https://ebankily-tst.appspot.com/payment"
headers = {
    f"Authorization :  Bearer {token}"
    "Content-type : application/json"
}

body = {
    "clientPhone": data.get("clientPhone"),
    "passcode": data.get("passcode"),
    "operationId": data.get("operationId"),
    "amount": data.get("amount"),
    "language": data.get("language"),
}

response = requests.post(url, json=body, headers=headers)
return response.json()