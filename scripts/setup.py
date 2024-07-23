"""setup.py handles connecting your Spotify account to your Spotify Application.  """

# This script is used to connect to your Spotify account and your Spotify Application. It is used to gather all the
# variables needed to run the main script and places them in the secrets.json file.
#
# Example: [python setup.py]

import json  # For parsing the secrets.json file.
import base64  # For base64 encoding hyphenated client id and client secret string.
import urllib.parse  # For URL-encoding the redirect URI.
import webbrowser  # For opening the user authentication request link.
import subprocess  # For opening Spotify.exe.
import time  # For waiting while Spotify opens.
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)  # For handling user setup code when using local server redirect URI.
import requests  # For sending Spotify API requests.

# pylint: disable=C0103
# pylint: disable=W0702
# pylint: disable=W0603
# pylint: disable=W0201

# Local server variables.
http_server = None
user_setup_code = None

# secrets.json file variables.
secrets_json = {}


class Server(BaseHTTPRequestHandler):
    """Class to host local server for redirect URI."""

    def do_GET(self):
        """Handles Get Request."""
        global user_setup_code
        user_setup_code = self.path[7:]
        self.path = "../index.html"
        try:
            file_to_open = open(self.path, encoding="utf-8").read()
            self.send_response(200)
        except:
            print(self.path)
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))


print("Running setup.py")

# Loading secrets json file.
print("Loading secrets.json file")
with open("../data/secrets.json", "r", encoding="utf-8") as file:
    secrets_json = json.load(file)

# Hyphenating CLIENTID and CLIENTSECRET and base64 encoding string.
print("Building Base64 encoded client id and client secret")
hyphenated_id_secret = secrets_json["CLIENTID"] + ":" + secrets_json["CLIENTSECRET"]
hyphenated_id_secret_bytes = hyphenated_id_secret.encode("ascii")
hyphenated_id_secret_base64_bytes = base64.b64encode(hyphenated_id_secret_bytes)
hyphenated_id_secret_base64_string = hyphenated_id_secret_base64_bytes.decode("ascii")
secrets_json["BASE64IDSECRET"] = hyphenated_id_secret_base64_string
print("Base64 encoded client id and client secret: " + hyphenated_id_secret_base64_string)

# Encoding the URI for requests.
print("Encoding redirect URI for requests")
encoded_redirect_uri = urllib.parse.quote_plus(secrets_json["REDIRECTURI"])
secrets_json["ENCODEDREDIRECTURI"] = encoded_redirect_uri
print("Encoded redirect URI: " + encoded_redirect_uri)

# Checking if using local server implementation.
print("Checking if using local server implementation")
local_server_option = False
domain = secrets_json["REDIRECTURI"][:16]
port = secrets_json["REDIRECTURI"][17:]

# Setting up local server.
if domain == "http://localhost" and port.isnumeric():
    local_server_option = True
    print("Setting up local server")
    http_server = HTTPServer(("localhost", int(port)), Server)

# Sending user authentication request.
user_auth_request = (
    "https://accounts.spotify.com/authorize?response_type=code&client_id="
    + secrets_json["CLIENTID"]
    + "&redirect_uri="
    + secrets_json["ENCODEDREDIRECTURI"]
    + "&scope=user-read-playback-state%20user-modify-playback-state"
)
print("Sending user authentication request: " + user_auth_request)
webbrowser.open(user_auth_request)
print("The Spotify User Authentication Request link should now open in your browser")
print("If you haven't yet, login to Spotify and agree and accept the terms")
print("This is giving the app you created access to your personal Spotify account")
print("You will then be redirected to the redirect URI once you have accepted the terms")

# Gathering user setup code.
if local_server_option:
    print("Handling the code from the redirect URI page")
    print("You can now close the redirect URI page")
    http_server.handle_request()
    print("User Setup Code: " + user_setup_code)
else:
    print("This next step is time sensitive. Look in your web browser address bar on the redirect URI page")
    user_setup_code = input('Copy the long code after the "=" sign and enter it here: ')
    print("User Setup Code entered: " + user_setup_code)

# Token Request.
auth_url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": "Basic " + hyphenated_id_secret_base64_string}
data = {"grant_type": "authorization_code", "code": user_setup_code, "redirect_uri": secrets_json["REDIRECTURI"]}
print("Sending Request for access token and refresh token")
auth_response = requests.post(auth_url, headers=headers, data=data, timeout=10)
auth_response_data = auth_response.json()
print("Request response: ")
print(auth_response_data)
secrets_json["REFRESHTOKEN"] = auth_response_data["refresh_token"]

# Testing Spotify executable.
print("Opening Spotify Application")
subprocess.Popen(secrets_json["EXEPATH"])

print("Giving Spotify Application time to open")
time.sleep(5)

# Getting available Spotify devices.
query = "https://api.spotify.com/v1/me/player/devices"
access_token = auth_response_data["access_token"]
response = requests.get(
    query,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    },
    timeout=10,
)
response_json = response.json()
if len(response_json["devices"]) == 0:
    print("No devices currently opened under your Spotify account")
else:
    print("Device List: ")
    print(response_json["devices"])
    device_id = response_json["devices"][0]["id"]
    device_name = response_json["devices"][0]["name"]
    print("Using Device Id: " + device_id)
    print("Using Device Name: " + device_name)
    secrets_json["DEVICEID"] = device_id
    json_output = json.dumps(secrets_json, indent=2)
    with open("../data/secrets.json", "w", encoding="utf-8") as file:
        file.write(json_output)

# Updating secrets file with changes.
print("Updating secrets file with changes")
json_output = json.dumps(secrets_json, indent=2)
with open("../data/secrets.json", "w", encoding="utf-8") as file:
    file.write(json_output)

print("setup.py script is now complete")
print("Verify all the fields in secrets.json are filled in correctly")
