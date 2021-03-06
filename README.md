# spotifycoasters

## Description
The initial idea for this project first came about because I have a large collection of CD's. I keep most of them in my car which means I have a big box of CD cases taking up space at home. The original idea was to mount these CD cases on a wall and when they were pressed a switch behind them would be activated and the album would be played. At the same time, I wanted to do something similar with my Spotify playlists. I wanted to build custom cartridges, that when read, would play my Spotify playlists. At the time, I was also looking to buy some coasters. I decided this would be a great project to combine all three of these ideas. I decided to make NFC embedded coasters that when read by a NFC reader would play my favorite albums and playlists on Spotify!

Built using Python utilizing the Spotify API.

## Installation
This guide is for setting up NFC embedded coasters that will play albums and playlists on Spotify when read by a NFC reader. This is written in Python making use of the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package. In the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package documentation they require Python version 2.7 or 3.5 or newer. In  my implementation I am using Python version 3.9.6 and running this on a Windows 10 machine. The two minimum items you need to purchase to make use of this project are a NFC reader and NFC tags. The NFC reader I used was the [Sony RC-S380](https://www.amazon.com/gp/product/B00VR1WARC) NFC reader. The NFC tags I used were [NTAG215 tags](https://www.amazon.com/gp/product/B08G8KQLLB). You could use a different NFC reader and different tags, but before doing so thoroughly research them in the [nfcpy](https://nfcpy.readthedocs.io/en/latest/overview.html#supported-devices) documentation. You may need to make small adjustments to my code if you went with a different reader or different tags.

### Application Setup
- Open the file [secrets.json](./data/secrets.json) to enter values during this authentication process.
- Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
- Copy the application's Client ID and Client Secret and add them to the [secrets.json](./data/secrets.json) file in their respective fields, **CLIENTID** and **CLIENTSECRET**.
- Next add a redirect uri to your Spotify application's settings and to the [secrets.json](./data/secrets.json) file.
    - The easiest option is to use a local server to automatically process the request sent to the redirect uri. For example you could use "http://localhost:8000". The setup script will handle setting up this local server so you won't need to worry about that, you only need to provide the link. Make sure to follow the same format as the example. Use "http" instead of "https" and don't add an extra "/" at the end of the uri. The setup script is equipt to setup a local server on another port if port 8000 is already in use.
    - If using a local server is not an option with your network you can use any link as the redirect uri. You will just need to manually copy a code from the redirect link and enter it into a script prompt during setup. For example you could use "https://johnprovazek.com/spotifycoasters"
    - Add the redirect uri you selected to your Spotify Application. In the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) under your application select edit settings. In settings, under **Redirect URIs** enter your redirect uri. Click add and then click save.
    - Add the redirect uri you selected to your [secrets.json](./data/secrets.json) file under the **REDIRECTURI** field.
- Next find the path to your Spotify.exe program. Copy that path and add it to the **EXEPATH** field in the [secrets.json](./data/secrets.json) file. You may need to use forward slashes or need to escape any backslashes to get this to work. Here are two examples of my executable path that are correctly formatted:
    ```
    C:/Users/John/AppData/Roaming/Spotify/Spotify.exe
    C:\\Users\\John\\AppData\\Roaming\\Spotify\\Spotify.exe
    ```
- Your [secrets.json](./data/secrets.json) file should now look something like this:
    ```
    {
        "CLIENTID": "7cf1c1326s7842ed8e73d4r4bd4da095",
        "CLIENTSECRET": "6221f71bced947d8b3063b403r49ar20",
        "REDIRECTURI": "http://localhost:8000",
        "EXEPATH": "C:/Users/John/AppData/Roaming/Spotify/Spotify.exe",
        "BASE64IDSECRET": "",
        "ENCODEDREDIRECTURI": "",
        "REFRESHTOKEN": "",
        "DEVICEID": ""
    }
    ```
- Before running the setup script close out of Spotify on all applications such as desktop, phone, gaming consoles, etc. If the executable path is setup correctly and all other Spotify applications were closed it will set your device as the default playback device. If you weren't able to close out of Spotify on all your devices you will be able to set the default playback device manually later. 
- Run the script [setup.py](./scripts/setup.py). This script will do the heavy lifting of setting up your personal Spotify account to interact with your Spotify application. Shortly after running the script an authentication link will open in your browser. When the link opens, login to Spotify if you haven't already. Hit agree to accept the terms. You will then be redirected to the redirect uri. If you used a local server as your redirect uri the rest of the script will run to completion and will not need any input. You can close out of the redirect website. If you used another link as the redirect uri you will need to copy the code in the address bar of your browser. Copy the whole code after the "=" sign. Enter that code into the script at the prompt.
- Once the script is complete look through the output for any errors and look through the [secrets.json](./data/secrets.json) file to verify all the fields are populated correctly.

### Common Errors
- If you used a link and not the local server for the redirect uri your access token and refresh token request might have resulted in a timeout error due to the Authorization code expiring. You might have got a response such as *{'error': 'invalid_grant', 'error_description': 'Authorization code expired'}*. If this is the case, run the script again and quickly copy the code in the address bar and enter it in the script at the prompt.
- If the script is hanging something was likely messed up in the localhost setup. In the terminal first try entering *Ctrl + C*. If the script is still hanging you likely just need to visit the localhost server and that will kill the script. For example if your redirect uri was "http://localhost:8000" visit that site in a browser.
- If the Spotify.exe path wasn't correct you may get a *the system cannot find the file specified* error. If this is the case you will need to modify your Spotify.exe path.
- If you had multiple Spotify applications open when you ran [setup.py](./scripts/setup.py), you may have an incorrect **DEVICEID** in the file [secrets.json](./data/secrets.json). If this is the case you just need to change the **DEVICEID** field in the file [secrets.json](./data/secrets.json). When [setup.py](./scripts/setup.py) was ran it will have outputted the list of devices connected to your personal Spotify account. Use that list of devices to determine the correct **DEVICEID** to put in the file [secrets.json](./data/secrets.json)

### NFC Tags and Spotify Setup
- Next open [nfc_spot.json](./data/nfc_spot.json). This file is a mapping of the NFC tags to the Spotify media you would like to play. Here's an  example of what the [nfc_spot.json](./data/nfc_spot.json) could look like:
    ```
    {
        "0415914a403916": { "context_uri": "spotify:album:0pquf1NcG9FdiypBPwICu9"},
        "0415918aefd615": { "context_uri": "spotify:album:3THuBNp86ScbTXwpTmAbdw", "offset": { "position": 7 }, "position_ms": 296200},
        "0415918abbf315": { "context_uri": "spotify:playlist:6GbQis3GgcPUkFmjnrFfUX"},
        "0415919af80415": { "context_uri": "spotify:playlist:5ZYEAB4m4UxQCFUloDY9u8", "offset": {"uri": "spotify:track:6aBUnkXuCEQQHAlTokv9or"}},
        "0415919aa35915": { "context_uri": "spotify:show:7nl7iKCcIM32kD1fMvI9eF", "offset": {"uri": "spotify:episode:6L0UDoFKuUMP0Mmn9l7jIT"}},
        "04fb9989700000": { "context_uri": "spotify:artist:1wg0T50ugsycU3EyXm38ib"},
        "049f9a2b700000": "shuffle",
        "0451bd2b700000": "sequential"
    }
    ```
- The first section is a 14 character code unique to one NFC tag. The second section is the request body sent to the Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/).
- This script is also setup for two special NFC tag mappings. You can map NFC tags to either the string "shuffle" or "sequential". If these NFC tags are read they will enable or disable the shuffle feature on Spotify.
- To gather the codes in your NFC tags first start by plugging in your NFC Reader. Run the script [nfc_reader.py](./scripts/nfc_reader.py). This is a simple script to read in NFC tags and output the code associated with each tag. Copy the output codes and add them to the [nfc_spot.json](./data/nfc_spot.json) file. Keep the format consistent with the example above.
- To create the corresponding Spotify section start by opening Spotify. Under playlists, albums, songs, artists, shows, and episodes there will be an ellipses. Click on that ellipses and select share and copy link. In the link there will be a section indicating whether it is a playlist, album, song, artist, show, or episode. Following that there is a 22 character code. You will use that media type and code to form a context_uri. For example when sharing the 1992 album Facing Future by Israel Kamakawiwo'ole the Spotify share link will look like: "https://open.spotify.com/album/0pquf1NcG9FdiypBPwICu9?si=jgPtKX9RSxWQi437n3rj7g". When formatting that link into a context_uri it will look like "spotify:album:0pquf1NcG9FdiypBPwICu9". You can then add that context_uri to correspond with an NFC tag in the [nfc_spot.json](./data/nfc_spot.json) file. Keep the format consistent with the example above.
- If you are doing this for many albums and playlists you may want to use the script [link_uri_conversion.py](./scripts/link_uri_conversion.py) to help. First put all the Spotify share links into a file. Then run the script [link_uri_conversion.py](./scripts/link_uri_conversion.py) with the file path as the first argument. This will convert all the Spotify share links and output them in the context_uri format.
- The Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/) appears to only be able to play albums, playlists, shows, and artists. If you want to play an individual song you will need to play it from an album or playlist. If you want to play a specific podcast episode you will need to do that from a show. There is an offset field to help with that. Check the example [nfc_spot.json](./data/nfc_spot.json) above to see some offset examples. It is worth noting that the offset position is indexed at 0. So if you wanted to play the 5th track of an album you would need to put 4 as the offset position.

### Coaster Setup
- If you decided to use coasters for this project here is the [youtube](https://www.youtube.com/watch?v=RV7-3CawKAM&t=68s&ab_channel=DIYPETE) tutorial I followed.
- In his tutorial he used felt pads on the bottom, I opted for a [cork backing](https://www.amazon.com/gp/product/B0834MWWS8/). There is probably a better way to do this, but I used an X-Acto knife to cut away a small cavity for the NFC tag to sit. I then hot glued the cork backing to the coaster such that you couldn't see the NFC tag.
- I printed out my album covers and playlist covers on 4x6 prints then cut them out and put them on the 4 inch tile coaster. I included a script [convert_album_cover.py](./scripts/convert_album_cover.py) to help convert square images to fit in 4x6 prints. This is assuming you are using 4 inch tiles. To use this script, first crop all your images so they are exact squares then put all the images in a directory. Run the script [convert_album_cover.py](./scripts/convert_album_cover.py) with the first argument as your source directory and the second argument as your destination directory. The script will convert all the images to the 4x6 format and place them in the destination directory.


## Usage
- To test this out and verify everything is working correctly run the script [spotify_coasters.py](./scripts/spotify_coasters.py). When your NFC tags are read they should now play the corresponding Spotify section in the [nfc_spot.json](./data/nfc_spot.json) file.
- If you are on a Windows machine, follow these steps to get this to script to run in the background on startup:
    - In [spotify_coasters.py](./scripts/spotify_coasters.py) there should be a line of code commented out running the function os.chdir. Uncomment that function and enter in the complete path to the directory of this script. You may need to escape backslashes in your path.
    - In [spotify_coasters.bat](./scripts/spotify_coasters.bat) replace the path with the complete path to the [spotify_coasters.py](./scripts/spotify_coasters.py) file.
    - In [spotify_coasters.vbs](./scripts/spotify_coasters.vbs) replace the path with the complete path to the [spotify_coasters.bat](./scripts/spotify_coasters.bat) file.
    - Open the Registry Editor and navigate to "Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    - Right click and select new and then select string value. Name this entry whatever you like.
    - Right click this new item and select modify. Enter in the complete path to the [spotify_coasters.vbs](./scripts/spotify_coasters.vbs) file.
    - Now when you restart your computer the [spotify_coasters.py](./scripts/spotify_coasters.py) script will be running in the background.

## Credits

[Spotify API](https://developer.spotify.com/console/) was used to interact with Spotify.

[nfcpy](https://nfcpy.readthedocs.io/en/latest/) was used for reading the NFC tags.

[Automate Spotify with Python (Spotify API) - Euan Morgan](https://www.youtube.com/watch?v=-FsFT6OwE1A&t=450s&ab_channel=EuanMorgan) was extremely helpful in understanding the Spotify API.

[How to Make Coasters - DIY Gift Ideas - DIY PETE](https://www.youtube.com/watch?v=RV7-3CawKAM&t=68s&ab_channel=DIYPETE) was helpful for learning how to make custom coasters

[Python Automation project : Run Python scripts Automatically in backgroud on windows startup - Code Bear](https://www.youtube.com/watch?v=XWV9tatoPQI&ab_channel=CodeBear) was helpful in understanding how to run this script on startup.

## Bugs & Improvements

- Script terminates when the NFC reader is unplugged. 