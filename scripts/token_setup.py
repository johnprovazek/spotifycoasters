import json # For parsing secrets.json file
import requests # For sending Spotify API requests

# Loading secrets json file
file = open('../data/secrets.json','r+')
secrets_json = json.load(file)

# Token Request
AUTH_URL = 'https://accounts.spotify.com/api/token'
headers = {
    "Authorization": "Basic " + secrets_json["BASE64IDSECRET"]
}
data = {
    'grant_type': 'authorization_code',
    'code': secrets_json["USERSETUPCODE"],
    'redirect_uri': secrets_json["REDIRECTURI"]
}
print("Sending Request for access token and refresh token")
auth_response = requests.post(AUTH_URL, headers=headers, data=data)
auth_response_data = auth_response.json()
print("Request response: ")
print(auth_response_data)
secrets_json["ACCESSTOKEN"] = auth_response_data['access_token']
secrets_json["REFRESHTOKEN"] = auth_response_data['refresh_token']

# Updating secrets file with changes
file.seek(0)
json.dump(secrets_json, file, indent = 4)

