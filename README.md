# spotifycoasters

## Description

This project implements NFC embedded drink coasters that when read by an NFC reader will play corresponding albums and playlists on Spotify.

Built using Python utilizing the Spotify API and nfcpy package.

<div align="center">
  <picture>
    <img src="https://github.com/user-attachments/assets/14458734-a6fe-4503-8b5b-25c0bacdbe09" width="830px">
  </picture>
</div>

## Installation

This guide is for setting up NFC embedded coasters that will play albums and playlists on Spotify when read by an NFC reader. This project is written in Python making use of the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package. In the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package documentation they require Python version 2.7 or 3.5 or newer. This has been tested using Python version 3.9.6 running on a Windows device. This project and guide has been designed for setting up on a Windows device. If you are using a different operating system you may need to make some adjustments to get this project to work. The two minimum items you need to purchase to make use of this project are an NFC reader and NFC tags. This project has been tested with the [Sony RC-S380](https://www.amazon.com/gp/product/B00VR1WARC) NFC reader and [NTAG215](https://www.amazon.com/gp/product/B08G8KQLLB) NFC tags. You could use a different NFC reader or different tags, but before doing so thoroughly research them in the [nfcpy supported devices documentation](https://nfcpy.readthedocs.io/en/latest/overview.html#supported-devices). You may need to make small adjustments to this project if you went with a different reader or different tags. Before moving on to this projects setup instructions follow the [nfcpy getting started instructions](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#installation) to setup [nfcpy](https://nfcpy.readthedocs.io/en/latest/) and configure your NFC reader.

### Spotify Developer App Setup

- Start by creating a new application in the [Spotify for Developers](https://developer.spotify.com/) page.
- Once logged in to the [Spotify for Developers](https://developer.spotify.com/) page, navigate to the application dashboard under the user dropdown in the upper right hand corner.
- Select `Create App`.
- Give your app a name and description. You can ignore the website field.
- For the redirect URI field you have two options to pick from. Either use this projects local server setup or you can enter any valid link in this field.
- The easiest option is to use a local server to automatically process the request that will be sent to the redirect URI later during setup. For the local server setup you could use the link `http://localhost:8000` for example. This project's setup script will handle setting up this local server so you won't need to worry about that, you only need to provide the link. Make sure to follow the same format as the example above. Use `http` instead of `https` and don't add an extra `/` at the end of the URI. The setup script is equip to setup a local server on another port if port `8000` is already in use.
- If using a local server is not an option with your network you can use any link as the redirect URI. You will just need to manually copy a code from the redirect link and enter it into a script prompt during setup. For example you could use the link `https://johnprovazek.com/spotifycoasters` in the redirect URI field.
- At the prompt `Which API/SDKs are you planning to use?`, select `Web API`.
- Once these fields are all complete and you have agreed to Spotify's terms of service click save to build your new Spotify application.

### Local Setup

- Open the file [secrets.json](./data/secrets.json) to enter values during this setup process.
- Add the same redirect URI you entered in the Spotify application to your [secrets.json](./data/secrets.json) file under the **REDIRECTURI** field.
- Navigate to the settings page for your Spotify application. In the settings page you will find your Spotify application's Client ID and Client Secret.
- Copy your Spotify application's Client ID and Client Secret and add them to the [secrets.json](./data/secrets.json) file in their respective fields, **CLIENTID** and **CLIENTSECRET**.
- Next find the path on your computer to your Spotify.exe program. Copy that path and add it to the **EXEPATH** field in the [secrets.json](./data/secrets.json) file. Windows uses backslashes in their file paths. Make sure your file path either uses forward slashes or has any backslashes escaped.
- Your [secrets.json](./data/secrets.json) file should now look something like this:
  ```json
  {
    "REDIRECTURI": "http://localhost:8000",
    "CLIENTID": "7cf1c1326s7842ed8e73d4r4bd4da095",
    "CLIENTSECRET": "6221f71bced947d8b3063b403r49ar20",
    "EXEPATH": "C:/Change/Path/Spotify.exe",
    "BASE64IDSECRET": "",
    "ENCODEDREDIRECTURI": "",
    "REFRESHTOKEN": "",
    "DEVICEID": ""
  }
  ```
- The next step is to run the [setup.py](./scripts/setup.py) script. Before running this script close out of Spotify on all applications such as desktop, phone, gaming consoles, etc. This is needed to ensure your Windows device will be setup as the default playback device.
- You can now run the script [setup.py](./scripts/setup.py). This script will do the heavy lifting of setting up your personal Spotify account to interact with your Spotify application. Shortly after running the script an authentication link will open in your browser. When the link opens, login to Spotify if you haven't already. Hit agree to accept the terms. You will then be redirected to the redirect URI. If you used a local server as your redirect URI the rest of the script will run to completion and will not need any input. You can close out of the redirect website. If you used another link as the redirect URI you will need to copy the code in the address bar of your browser. Copy the long code after the `=` sign. Enter that code into the script at the prompt.
- Once the script is complete look through the output for any errors and look through the [secrets.json](./data/secrets.json) file to verify all the fields are populated correctly.

### Common Errors

- If you used a link and not the local server for the redirect URI your access token and refresh token request might have resulted in a timeout error due to the Authorization code expiring. You might have got a response such as _{'error': 'invalid_grant', 'error_description': 'Authorization code expired'}_. If this is the case, run the script again and quickly copy the code in the address bar and enter it in the script at the prompt.
- If the script is hanging something was likely messed up in the localhost setup. In the terminal first try entering _Ctrl + C_ to stop the script execution. If the script is still hanging you likely just need to visit the localhost server and that will kill the script. So if your redirect URI was `http://localhost:8000` visit that site in a browser. Once this is resolved try running the [setup.py](./scripts/setup.py) script again. If this fails again try using a link as the redirect URI instead of the local server setup.
- If the Spotify.exe path wasn't setup correctly you may get a _the system cannot find the file specified_ error. If this is the case you will need to modify your Spotify.exe path.
- If you had multiple Spotify applications open when you ran the [setup.py](./scripts/setup.py) script you may have an incorrect **DEVICEID** in the file [secrets.json](./data/secrets.json). If this is the case you just need to change the **DEVICEID** field in the file [secrets.json](./data/secrets.json). When the [setup.py](./scripts/setup.py) script was ran it will have outputted the list of devices connected to your personal Spotify account. Use that list of devices to determine the correct **DEVICEID** to put in the file [secrets.json](./data/secrets.json).

### NFC Tags and Spotify Setup

- Open the file [nfc_spot.json](./data/nfc_spot.json). This file is a mapping of your NFC tags to the corresponding Spotify media you would like to play. Below is an example of a valid [nfc_spot.json](./data/nfc_spot.json) file showcasing different media types available to play:
  ```json
  {
    "0415914a403916": { "context_uri": "spotify:album:0pquf1NcG9FdiypBPwICu9" },
    "0415918aefd615": {
      "context_uri": "spotify:album:3THuBNp86ScbTXwpTmAbdw",
      "offset": { "position": 7 },
      "position_ms": 296200
    },
    "0415918abbf315": {
      "context_uri": "spotify:playlist:6GbQis3GgcPUkFmjnrFfUX"
    },
    "0415919af80415": {
      "context_uri": "spotify:playlist:5ZYEAB4m4UxQCFUloDY9u8",
      "offset": { "uri": "spotify:track:6aBUnkXuCEQQHAlTokv9or" }
    },
    "0415919aa35915": {
      "context_uri": "spotify:show:7nl7iKCcIM32kD1fMvI9eF",
      "offset": { "uri": "spotify:episode:6L0UDoFKuUMP0Mmn9l7jIT" }
    },
    "04fb9989700000": {
      "context_uri": "spotify:artist:1wg0T50ugsycU3EyXm38ib"
    },
    "049f9a2b700000": "shuffle",
    "0451bd2b700000": "sequential"
  }
  ```
- The first section is a 14 character code unique to one NFC tag. The second section is the request body sent to the Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/).
- This script is also setup for two special NFC tag mappings. You can map NFC tags to either the string "shuffle" or "sequential". If these NFC tags are read they will enable or disable the shuffle feature on Spotify. This projects playback behavior is to play all albums sequentially and play all playlists shuffled.
- To gather the codes in your NFC tags first start by plugging in your NFC Reader. Run the script [nfc_reader.py](./scripts/nfc_reader.py). This is a simple script to read in NFC tags and output the code associated with each tag. Copy the output codes and add them to the [nfc_spot.json](./data/nfc_spot.json) file. Keep the format consistent with the example above.
- To create the corresponding Spotify section start by opening Spotify. Find a playlist or album and look for an ellipses. Click on that ellipses and select share and copy link. In the link you have copied there will be a section indicating whether it is a playlist, album, song, artist, show, episode, etc. Following that there is a 22 character code. You will use that media type and code to form a context_uri. For example when sharing the 1992 album Facing Future by Israel Kamakawiwo'ole the Spotify share link will look something like: `https://open.spotify.com/album/0pquf1NcG9FdiypBPwICu9?si=jgPtKX9RSxWQi437n3rj7g`. When formatting that link into a context_uri it will look like `spotify:album:0pquf1NcG9FdiypBPwICu9`. You can then add that context_uri to correspond with an NFC tag in the [nfc_spot.json](./data/nfc_spot.json) file. Keep the format consistent with the example above.
- If you are doing this for many albums and playlists you may want to use the script [link_uri_conversion.py](./scripts/link_uri_conversion.py) to help. First put all the Spotify share links into a file. Then run the script [link_uri_conversion.py](./scripts/link_uri_conversion.py) with the file path as the first argument. This will convert all the Spotify share links and output them in the context_uri format.
- The Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/) appears to only be able to play albums, playlists, shows, and artists. If you want to play an individual song you will need to play it from an album or playlist. If you want to play a specific podcast episode you will need to do that from a show. There is an offset field to help with that. Check the example [nfc_spot.json](./data/nfc_spot.json) above to see some offset examples. It is worth noting that the offset position is indexed at 0. So if you wanted to play the 5th track of an album you would need to put 4 as the offset position.

### Coaster Setup

- If you decided to use coasters for this project here is a helpful [youtube tutorial](https://youtu.be/RV7-3CawKAM) to follow.
- In his [tutorial](https://youtu.be/RV7-3CawKAM) he used felt pads on the bottom of the coaster. Instead of felt pads you could use a [cork backing](https://www.amazon.com/gp/product/B0834MWWS8/) and use an X-Acto knife to cut a small cavity for the NFC tag to sit.
- Once you have the NFC tag placed in the cavity hot glue the backing to the coaster so that you can no longer see the NFC tag.
- The next step is to print out your album covers and playlist covers on 4x6 photo prints.
- Then cut them out and use mod podge to attach them on the 4 inch tile coasters.
- Included in this project is a script [convert_album_cover.py](./scripts/convert_album_cover.py) to help convert square images to fit in 4x6 photo prints. To use this script, first crop all your images so they are exact squares then put all the images in a directory. Run the script [convert_album_cover.py](./scripts/convert_album_cover.py) with the first argument as your source directory and the second argument as your destination directory. The script will convert all the images to the 4x6 photo print format and place them in the destination directory.

## Usage

- To test this out and verify everything is working correctly run the script [spotify_coasters.py](./scripts/spotify_coasters.py). When your NFC tags are read they should now play the corresponding Spotify media found in the [nfc_spot.json](./data/nfc_spot.json) file.
- If you would like to run this script in the background on startup you need to add the [spotify_coasters.vbs](./scripts/spotify_coasters.vbs) script to the Windows startup folder.
- In the [spotify_coasters.vbs](./scripts/spotify_coasters.vbs) script update the _scriptPath_ variable with the full path to the [spotify_coasters.py](./scripts/spotify_coasters.py) file.
- Uncomment the code in [spotify_coasters.vbs](./scripts/spotify_coasters.vbs) then move this file to the Windows startup folder.
- The Windows startup folder can be found by typing `WindowsKey + R` and entering `shell:startup`.
- The last step is to add the full path of this projects [scripts](./scripts/) directory to the _os.chdir_ command in the the file [spotify_coasters.py](./scripts/spotify_coasters.py).
- You can now restart your device and test that this is working.

## Credits

[Spotify API](https://developer.spotify.com/console/) was used to interact with Spotify.

[nfcpy](https://nfcpy.readthedocs.io/en/latest/) was used for reading the NFC tags.

[Automate Spotify with Python (Spotify API) - Euan Morgan](https://youtu.be/-FsFT6OwE1A) was extremely helpful in understanding the Spotify API.

[How to Make Coasters - DIY Gift Ideas - DIY PETE](https://youtu.be/RV7-3CawKAM) was helpful for learning how to make custom coasters.

## Bugs & Improvements

- Script terminates when the NFC reader is unplugged.
- Improve error handling.
