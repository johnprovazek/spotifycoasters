import json
from random import shuffle # For parsing secrets.json file
import requests # For sending Spotify API requests
import nfc # For reading NFC tags
import subprocess  # For opening Spotify.exe and checking if it is open
import re # Using regex to get Spotify medium type from the context_uri
import time # For refreshing the Spotify API access token every hour and waiting while Spotify opens
import threading # For spinning up a thread to handle the NFC reader and tokens
import sys # Using sys to terminate the script upon Ctrl + C
import os # For setting the current directory when launching script on startup

class SpotifyCoasters:
    def __init__(self):
        print ("Loading in secrets")
        self.base_64 = secrets_json["BASE64IDSECRET"]
        self.access_token = ""
        self.refresh_token = secrets_json["REFRESHTOKEN"]
        self.device_name = secrets_json["DEVICENAME"]
        self.device_id = secrets_json["DEVICEID"]

    def play(self,tag):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})
        response_json = response.json()
        data = nfc_spot_json[tag.identifier.hex()]
        if response_json["shuffle_state"]:
            data ={'context_uri':data["context_uri"]}
            print(data)
        self.launch_desktop_spotify()
        print("Sending request to play Spotify content")
        query = "https://api.spotify.com/v1/me/player/play?device_id=" + self.device_id
        response = requests.put(query, data = json.dumps(data),
            headers={"Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)})
        self.print_context(tag)
        # print(response)

    def refresh_access_token(self):
        print("Refreshing Spotify token")
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers={"Authorization": "Basic " + self.base_64})
        response_json = response.json()
        self.access_token = response_json["access_token"]

    def launch_desktop_spotify(self):
        open_processes = subprocess.check_output('tasklist', shell=True)
        if "Spotify.exe" not in str(open_processes):
            print ("Opening Spotify Application")
            subprocess.Popen(secrets_json["EXEPATH"])
            time.sleep(5)

    def print_context(self,tag):
        context_uri = nfc_spot_json[tag.identifier.hex()]["context_uri"]
        spotify_id = context_uri[-22:]
        spotify_medium_type = re.search(":(.*?):", context_uri).group(1)
        if(spotify_medium_type == "album"):
            query = "https://api.spotify.com/v1/albums/" + spotify_id
            response = requests.get(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})
            response_json = response.json()
            album_name = response_json["name"]
            album_year = response_json["release_date"][0:4]
            album_artists = ""
            album_artists_len = len(response_json["artists"])-1
            for artist in response_json["artists"]:
                if response_json["artists"].index(artist) == 0:
                    album_artists = album_artists + artist["name"]
                elif response_json["artists"].index(artist) == album_artists_len:
                    album_artists = album_artists + ", and " + artist["name"]
                else:
                    album_artists = album_artists + ", " + artist["name"]
            print("Playing Album: " + album_name + " (" + album_year + ") by " + album_artists)
        elif(spotify_medium_type == "playlist"):
            query = "https://api.spotify.com/v1/playlists/" + spotify_id
            response = requests.get(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})
            response_json = response.json()
            playlist_name = response_json["name"]
            playlist_creator = response_json["owner"]["display_name"]
            print("Playing Playlist: " + playlist_name + " by " +  playlist_creator)
        elif(spotify_medium_type == "show"):
            query = "	https://api.spotify.com/v1/shows/" + spotify_id
            response = requests.get(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})
            response_json = response.json()
            podcast_name = response_json["name"]
            print("Playing Podcast: " + podcast_name)
        elif(spotify_medium_type == "artist"):
            query = "	https://api.spotify.com/v1/artists/" + spotify_id
            response = requests.get(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})
            response_json = response.json()
            artist_name = response_json["name"]
            print("Playing Artist: " + artist_name)
        else:
            print("Error: Spotify Content was incorrectly setup in your nfc_spot.json file. In your context_uri you should have album, playlist, show, or artist")

    def set_shuffle(self, state):
        query = "https://api.spotify.com/v1/me/player/shuffle?state=" + state + "&device_id=" + self.device_id
        response = requests.put(query,
                headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)})

    def nfc_reader_on_tag_connect(self, tag):
        print("\nTag Connected: " + tag.identifier.hex())
        if tag.identifier.hex() in nfc_spot_json:
            if nfc_spot_json[tag.identifier.hex()] == "shuffle":
                print("Turning on Shuffle")
                self.set_shuffle("true")
            elif nfc_spot_json[tag.identifier.hex()] == "sequential":
                print("Turning off Shuffle")
                self.set_shuffle("false")
            else:
                self.play(tag)
        else:
            print("The Tag: " + tag.identifier.hex() + " is not listed in nfc_spot.json")
        return True

    def nfc_reader_on_tag_release(self, tag):
        print("Tag Disconnected: " + tag.identifier.hex())

    def nfc_reader_spin_up(self):
        print ("NFC Reader starting up in child thread")
        clf = nfc.ContactlessFrontend('usb')
        clf.connect(rdwr={'on-release': self.nfc_reader_on_tag_release, 'on-connect': self.nfc_reader_on_tag_connect})

    def nfc_run_thread(self):
        reader_thread = threading.Thread(target=SpotifyCoasters.nfc_reader_spin_up, args = (self,) )
        reader_thread.daemon = True
        reader_thread.start()

# When launching the script on startup set the full path to your working directory
# os.chdir("C:\\Users\\John\\Documents\\spotifycoasters")

# Load the NFC tag and Spotify request data json file
nfc_spot_file = open('./john/nfc_spot.json')
nfc_spot_json = json.load(nfc_spot_file)

# Load the secrets json file
secrets_file = open('./john/secrets.json')
secrets_json = json.load(secrets_file)

# Initilize the Spotify Coaster project app
a = SpotifyCoasters()

# Refresh token. This is needed incase coaster is on NFC Reader on startup.
a.refresh_access_token()

# Start up the NFC reader loop in own thread
a.nfc_run_thread()

# Start refresh token loop that will refresh the access token every hour
while True:
    try:
        a.refresh_access_token()
        time.sleep(3480)
    except KeyboardInterrupt:
        print("\nCtrl + C registered")
        sys.exit()

