import json # For parsing secrets.json file
import base64 # For base64 encoding hypenated client id and client secret string
import urllib.parse # For URL-encoding the redirect URI
import webbrowser # For opening the User Authentication Request link

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

# Creating user authentication request
user_auth_request = "https://accounts.spotify.com/authorize?response_type=code&client_id=" + secrets_json["CLIENTID"] + "&redirect_uri=" + secrets_json["ENCODEDREDIRECTURI"] + "&scope=user-read-playback-state%20user-modify-playback-state"
print("\nUser Authentication Request: " + user_auth_request)
webbrowser.open(user_auth_request)
print("\nThe Spotify User Authentication Request link should now open in your browser. If you haven't yet, login to Spotify. Next hit agree to accept the terms. This is giving the app you created access to your personal Spotify. You will then be redirected to the redirect uri. In the URL there will be a code, copy that code and add it to USERSETUPCODE in secrets.json. Next run the token_setup.py script. This is time sensative. If your authorization code expired, run this script again and repeat this process.")

# Updating secrets file with changes
file.seek(0)
json.dump(secrets_json, file, indent = 4)