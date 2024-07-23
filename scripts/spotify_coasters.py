"""spotify_coasters.py reads NFC tags and plays corresponding Spotify media. """

# This script is used to read NFC tags from an NFC reader. The script will then play the Spotify media associated with
# the NFC tag in nfc_sport.json.
#
# Example: [python spotify_coasters.py]

# pylint: disable=R0914

import json  # For parsing the secrets.json file.
import subprocess  # For opening Spotify.exe.
import re  # Using regex to get Spotify medium type from the context_uri.
import time  # For refreshing the Spotify API access token every hour and waiting while Spotify opens.
from datetime import datetime  # For keeping track of time the access token was issued.
import os  # For setting the current directory when launching script on startup.
import nfc  # For reading NFC tags.
import requests  # For sending Spotify API requests.


class SpotifyCoasters:
    """Class to handle playing Spotify media corresponding to NFC tags."""

    def __init__(self):
        print("Initializing the Spotify Coasters application")
        self.access_token = ""
        self.access_token_date_time = datetime.min
        print("Loading in secrets")
        self.base_64 = secrets_json["BASE64IDSECRET"]
        self.refresh_token = secrets_json["REFRESHTOKEN"]
        self.device_id = secrets_json["DEVICEID"]

    def play(self, tag):
        """Play Spotify media."""
        context_uri = nfc_spot_json[tag.identifier.hex()]["context_uri"]
        spotify_media_type = re.search(":(.*?):", context_uri).group(1)
        self.launch_desktop_spotify()
        # Albums will be played sequentially.
        if spotify_media_type == "album":
            self.set_shuffle("false")
        # Playlists will be played shuffled.
        elif spotify_media_type == "playlist":
            self.set_shuffle("true")
        data = nfc_spot_json[tag.identifier.hex()]
        print("Sending request to play Spotify content")
        query = "https://api.spotify.com/v1/me/player/play?device_id=" + self.device_id
        requests.put(
            query,
            data=json.dumps(data),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )
        self.print_context(context_uri, spotify_media_type)

    def print_context(self, context_uri, spotify_media_type):
        """Outputs information about the context_uri played."""
        spotify_id = context_uri[-22:]
        if spotify_media_type == "album":
            query = "https://api.spotify.com/v1/albums/" + spotify_id
            response = requests.get(
                query,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
            response_json = response.json()
            album_name = response_json["name"]
            album_year = response_json["release_date"][0:4]
            album_artists = ""
            album_artists_len = len(response_json["artists"]) - 1
            for artist in response_json["artists"]:
                if response_json["artists"].index(artist) == 0:
                    album_artists = album_artists + artist["name"]
                elif response_json["artists"].index(artist) == album_artists_len:
                    album_artists = album_artists + ", and " + artist["name"]
                else:
                    album_artists = album_artists + ", " + artist["name"]
            print("Playing Album: " + album_name + " (" + album_year + ") by " + album_artists)
        elif spotify_media_type == "playlist":
            query = "https://api.spotify.com/v1/playlists/" + spotify_id
            response = requests.get(
                query,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
            response_json = response.json()
            playlist_name = response_json["name"]
            playlist_creator = response_json["owner"]["display_name"]
            print("Playing Playlist: " + playlist_name + " by " + playlist_creator)
        elif spotify_media_type == "show":
            query = "	https://api.spotify.com/v1/shows/" + spotify_id
            response = requests.get(
                query,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
            response_json = response.json()
            podcast_name = response_json["name"]
            print("Playing Podcast: " + podcast_name)
        elif spotify_media_type == "artist":
            query = "	https://api.spotify.com/v1/artists/" + spotify_id
            response = requests.get(
                query,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
            response_json = response.json()
            artist_name = response_json["name"]
            print("Playing Artist: " + artist_name)
        else:
            print("Error: Spotify Content was incorrectly setup in your nfc_spot.json file")
            print("In your context_uri you should have album, playlist, show, or artist")

    def refresh_access_token(self):
        """Handles refreshing the Spotify access token."""
        cur_time = datetime.now()
        difference = cur_time - self.access_token_date_time
        if difference.total_seconds() > 3300:
            self.access_token_date_time = cur_time
            print("Refreshing Spotify token")
            query = "https://accounts.spotify.com/api/token"
            response = requests.post(
                query,
                data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
                headers={"Authorization": "Basic " + self.base_64},
                timeout=10,
            )
            response_json = response.json()
            self.access_token = response_json["access_token"]

    def launch_desktop_spotify(self):
        """Opens up Spotify desktop application."""
        open_processes = subprocess.check_output("tasklist", shell=True)
        if "Spotify.exe" not in str(open_processes):
            print("Opening Spotify Application")
            subprocess.Popen(secrets_json["EXEPATH"])
            time.sleep(5)

    def set_shuffle(self, state):
        """Changes Spotify shuffle value."""
        query = "https://api.spotify.com/v1/me/player/shuffle?state=" + state + "&device_id=" + self.device_id
        requests.put(
            query,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )

    def nfc_reader_on_tag_connect(self, tag):
        """Handles when an NFC tag makes connection with the NFC reader."""
        self.refresh_access_token()
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
        """Handles when an NFC tag is no longer connected with the NFC reader."""
        print("Tag Disconnected: " + tag.identifier.hex())

    def nfc_reader_spin_up(self):
        """Handles setting up the NFC reader."""
        print("Connecting usb NFC Reader")
        clf = nfc.ContactlessFrontend("usb")
        print("Ready to accept coasters")
        clf.connect(rdwr={"on-release": self.nfc_reader_on_tag_release, "on-connect": self.nfc_reader_on_tag_connect})


# When launching the script on startup set the full path to your working directory.
# os.chdir("C:/Change/Path/spotifycoasters/scripts")

# Load nfc_spot.json file containing the NFC tag and Spotify request data.
print("Loading in the nfc_spot.json file")
nfc_spot_file = open("../data/nfc_spot.json", encoding="utf-8")
nfc_spot_json = json.load(nfc_spot_file)

# Load the secrets.json file.
print("Loading in the secrets.json file")
secrets_file = open("../data/secrets.json", encoding="utf-8")
secrets_json = json.load(secrets_file)

# Initialize the Spotify Coasters application.
app = SpotifyCoasters()

# Refreshing access token.
app.refresh_access_token()

# Start up the NFC reader.
app.nfc_reader_spin_up()
