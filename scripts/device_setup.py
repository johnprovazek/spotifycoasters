import json # For parsing secrets.json file
import requests # For sending Spotify API requests
import subprocess # For opening Spotify.exe
import time # For waiting while Spotify opens

# Loading secrets json file
file = open('../data/secrets.json','r+')
secrets_json = json.load(file)

# Testing Spotify executable
print ("Opening Spotify Application")
subprocess.Popen(secrets_json["EXEPATH"])
time.sleep(5)

# Refreshing token
print("Refreshing Spotify token")
query = "https://accounts.spotify.com/api/token"
response = requests.post(query,
    data={"grant_type": "refresh_token", "refresh_token": secrets_json["REFRESHTOKEN"]},
    headers={"Authorization": "Basic " + secrets_json["BASE64IDSECRET"]})
response_json = response.json()
access_token = response_json["access_token"]

# Getting avaiable Spotify devices
query = "https://api.spotify.com/v1/me/player/devices"
response = requests.get(query,
    headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)})
response_json = response.json()
if len(response_json["devices"]) == 0:
    print("\nNo devices currently opened under your Spotify account")
else:
    print("Device List: ")
    print(response_json["devices"])
    device_id = response_json["devices"][0]["id"]
    device_name = response_json["devices"][0]["name"]
    print("Using Device Id: " + device_id)
    print("Using Device Name: " + device_name)
    secrets_json["DEVICEID"] = device_id
    secrets_json["DEVICENAME"] = device_name
    file.seek(0)
    json.dump(secrets_json, file, indent = 4)
