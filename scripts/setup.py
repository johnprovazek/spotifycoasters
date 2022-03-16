import json # For parsing secrets.json file
import base64 # For base64 encoding hypenated client id and client secret string
import urllib.parse # For URL-encoding the redirect URI
import webbrowser # For opening the User Authentication Request link
import requests # For sending Spotify API requests
import subprocess # For opening Spotify.exe
import time # For waiting while Spotify opens
from http.server import HTTPServer, BaseHTTPRequestHandler # For handling user setup code when using local server redirect uri

# Local server variables
httpd = None
user_setup_code = None

# Class to host local server for redirect uri
class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        global user_setup_code
        user_setup_code = self.path[7:]
        self.path = '../web/index.html'
        try:
            file_to_open = open(self.path).read()
            self.send_response(200)
        except:
            print(self.path)
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

# Loading secrets json file
file = open('../data/secrets.json','r+')
secrets_json = json.load(file)

# Hyphenating CLIENTID and CLIENTSECRET and base64 encoding string.
hyphenated_id_secret = secrets_json["CLIENTID"] + ":" + secrets_json["CLIENTSECRET"]
hyphenated_id_secret_bytes = hyphenated_id_secret.encode("ascii")
hyphenated_id_secret_base64_bytes = base64.b64encode(hyphenated_id_secret_bytes)
hyphenated_id_secret_base64_string = hyphenated_id_secret_base64_bytes.decode("ascii")
secrets_json["BASE64IDSECRET"] = hyphenated_id_secret_base64_string
print("\nBASE64 Encoded ID and Secret: " + hyphenated_id_secret_base64_string)

# Encoding the url for requests
encoded_redirect_uri = urllib.parse.quote_plus(secrets_json["REDIRECTURI"])
secrets_json["ENCODEDREDIRECTURI"] = encoded_redirect_uri
print("\nEncoded Redirect URI: " + encoded_redirect_uri)

# Checking if using local server implementation. If so launching local server.
localserveroption = False
domain = secrets_json["REDIRECTURI"][:16]
port = secrets_json["REDIRECTURI"][17:]

if domain == "http://localhost" and port.isnumeric():
    localserveroption = True
    httpd = HTTPServer(('localhost',int(port)),Serv)

# Creating user authentication request
user_auth_request = "https://accounts.spotify.com/authorize?response_type=code&client_id=" + secrets_json["CLIENTID"] + "&redirect_uri=" + secrets_json["ENCODEDREDIRECTURI"] + "&scope=user-read-playback-state%20user-modify-playback-state"
print("\nUser Authentication Request: " + user_auth_request)
webbrowser.open(user_auth_request)
print("\nThe Spotify User Authentication Request link should now open in your browser. If you haven't yet, login to Spotify. Next hit agree to accept the terms. This is giving the app you created access to your personal Spotify. You will then be redirected to the redirect uri once you accept the terms.")

# Gathering user setup code
if localserveroption:
    print("\nHandling the code from the redirect uri page. You can now close that page.")
    httpd.handle_request()
    print("\nUser Setup Code: " + user_setup_code)
else:
    user_setup_code = input("\nThis next step is time sensitive. Look in your web browser address bar on the redirect uri page. Copy the whole code after the \"=\" sign and enter it here:")
    print("\nUser Setup Code Entered: " + user_setup_code)

# {'error': 'invalid_grant', 'error_description': 'Invalid authorization code'}

# Token Request
AUTH_URL = 'https://accounts.spotify.com/api/token'
headers = {
    "Authorization": "Basic " + hyphenated_id_secret_base64_string
}
data = {
    'grant_type': 'authorization_code',
    'code': user_setup_code,
    'redirect_uri': secrets_json["REDIRECTURI"]
}
print("\nSending Request for access token and refresh token")
auth_response = requests.post(AUTH_URL, headers=headers, data=data)
auth_response_data = auth_response.json()
print("\nRequest response: ")
print(auth_response_data)
secrets_json["REFRESHTOKEN"] = auth_response_data['refresh_token']

# Testing Spotify executable
print ("\nOpening Spotify Application")
subprocess.Popen(secrets_json["EXEPATH"])

print ("\nGiving Spotify Application time to open")
time.sleep(5)

# Getting avaiable Spotify devices
query = "https://api.spotify.com/v1/me/player/devices"
response = requests.get(query,
    headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(auth_response_data['access_token'])})
response_json = response.json()
if len(response_json["devices"]) == 0:
    print("\nNo devices currently opened under your Spotify account")
else:
    print("\nDevice List: ")
    print(response_json["devices"])
    device_id = response_json["devices"][0]["id"]
    device_name = response_json["devices"][0]["name"]
    print("\nUsing Device Id: " + device_id)
    print("\nUsing Device Name: " + device_name)
    secrets_json["DEVICEID"] = device_id
    file.seek(0)
    json.dump(secrets_json, file, indent = 4)

print("\nSetup Script Complete, verify all fields in secrets.json are filled correctly.")

# Updating secrets file with changes
file.seek(0)
json.dump(secrets_json, file, indent = 4)