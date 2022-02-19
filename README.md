# spotifycoasters

## Description
This project was originally concieved as a much different idea. This idea came about because I have a large collection of CD's. I keep most of them in my car which means I have a big box of CD cases at home taking up space. The original idea was to mount these CD cases on a wall. When the CD's would be pressed a switch behind them would be activated and the album would be played. At the same time I also wanted to do something similar with my Spotify playlists. I wanted to build custom cartridges that when read would play my Spotify playlists. At the time, I was also looking to buy some coasters and decided this would be a great project to combine all these ideas. I decided to make NFC embedded coasters that when read by a NFC reader would play my favorite albums and playlists on Spotify!

## Installation
This guide is for setting up NFC embedded coasters that will play albums and playlists on Spotify when read by a NFC reader. This is written in Python making use of the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package. In the [nfcpy](https://nfcpy.readthedocs.io/en/latest/) package documentation they require Python version 2.7 or 3.5 or newer. In  my implementation I am using Python version 3.9.6 and running this on a Windows 10 machine. The two minimum items you need to purchase to make use of this project are a NFC reader and NFC tags. The NFC reader I used was the [Sony RC-S380](https://www.amazon.com/gp/product/B00VR1WARC) NFC reader. The NFC tags I used were [NTAG215 tags](https://www.amazon.com/gp/product/B08G8KQLLB). You could use a different NFC reader and different tags, but before doing so thoroughly research in the [nfcpy](https://nfcpy.readthedocs.io/en/latest/overview.html#supported-devices) documentation to make sure the devices and tags are compatible. You may need to make adjustments to my code to get any different readers or tags than the ones I used to work.

### Application Setup
- Open the file [secrets.json](./data/secrets.json) to enter values during this authentication process.
- Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
- Copy the application's Client ID and Client Secret and add them to [secrets.json](./data/secrets.json) in their respective fields, **CLIENTID** and **CLIENTSECRET**.
- Next add a redirect uri to your Spotify application's settings and to [secrets.json](./data/secrets.json).
    - This redirect uri could be any link. It will only be used for setup. For example you may use: "http://buymeabeer.com/johnprovazek/" or "https://www.google.com/"
    - In the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) under your application select edit settings. Under **Redirect URIs** enter your redirect uri. Click add and then click save.
    - In [secrets.json](./data/secrets.json) enter the same redirect uri under the **REDIRECTURI** field.
- The next steps are time sensitive so read over them first before executing the scripts.
    - Run the Python script **user_auth_request.py**, this script will do some setup and open the Spotify User Authentication Request link in your browser. This is so your personal Spotify account is able to interact with your application. When the link opens, login to Spotify if you haven't already. Next hit agree to accept the terms. You will then be redirected to the redirect uri. In the URL bar of your browser there will be a code at the end of the url, copy that code and add it to the **USERSETUPCODE** field in [secrets.json](./data/secrets.json). Save the file.
    - Run the Python script **token_setup.py**, this will request an access token and refresh token for your application. This is time sensative. Check [secrets.json](./data/secrets.json) to verify the access token and refresh token were added. If your authorization code expired you will need to rerun these scripts and repeat the process.
- Find the path to your Spotify.exe program. Copy that path and add it to the **EXEPATH** field in [secrets.json](./data/secrets.json). You might need to escape any backslashes to get this to work. Here is my exe path for example:
    ```
    C:\\Users\\John\\AppData\\Roaming\\Spotify\\Spotify.exe
    ```
- Next we will run a script to setup the device you would like Spotify to playback on.
    - Close out of Spotify on all applications such as desktop, phone, gaming consoles, etc.
    - Run the Python script **device_setup.py**, this script will test the Spotify executable path you provided earlier. If the executable path is setup correctly and all other Spotify applications were closed it will set your device as the default playback device. This script works by sending a request to Spotify for the list of open devices and it will add the first one on the list to [secrets.json](./data/secrets.json). This script will also output the list of open devices. If the wrong device was setup all you need to change is the **DEVICENAME** and **DEVICEID** fields in [secrets.json](./data/secrets.json) with the correct device name and device id.

### NFC Tags and Spotify Setup
- Next open [nfc_spot.json](./data/nfc_spot.json). This file is a mapping of the NFC tags to the Spotify media we would like to play. Here's an  example of what the [nfc_spot.json](./data/nfc_spot.json) could look like:
    ```
    {
        "0415914a403916": { "context_uri": "spotify:album:0pquf1NcG9FdiypBPwICu9"},
        "0415918aefd615": { "context_uri": "spotify:album:3THuBNp86ScbTXwpTmAbdw", "offset": { "position": 7 }, "position_ms": 296200},
        "0415918abbf315": { "context_uri": "spotify:playlist:6GbQis3GgcPUkFmjnrFfUX"},
        "0415919af80415": { "context_uri": "spotify:playlist:5ZYEAB4m4UxQCFUloDY9u8", "offset": {"uri": "spotify:track:6aBUnkXuCEQQHAlTokv9or"}},
        "0415919aa35915": { "context_uri": "spotify:show:7nl7iKCcIM32kD1fMvI9eF", "offset": {"uri": "spotify:episode:6L0UDoFKuUMP0Mmn9l7jIT"}},
        "04fb9989700000": { "context_uri": "spotify:artist:1wg0T50ugsycU3EyXm38ib"}
    }
    ```
- The first section is a 14 character code unique to one NFC tag. The second section is the request body sent to the Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/).
- To gather the codes in your NFC tags first start by plugging in your NFC Reader. Run the Python script **nfc_reader.py**. This is a simple script to read in NFC tags and output the code associated with each tag. Copy the output and add it to [nfc_spot.json](./data/nfc_spot.json).
- To create the corresponding Spotify section start by opening Spotify. Under playlists, albums, songs, artists, shows, and episodes there will be an ellipses. Click on that ellipses and select share and copy link. In the link there will be a section indicating whether it is a playlist, album, song, artist, show, or episode. Following that there is a 22 character code. You will use that media type and code to form a context_uri. For example when I share the 1992 album Facing Future by Israel Kamakawiwo'ole the Spotify share link will look like: "https://open.spotify.com/album/0pquf1NcG9FdiypBPwICu9?si=jgPtKX9RSxWQi437n3rj7g". When I format that link into a context_uri it will look like "spotify:album:0pquf1NcG9FdiypBPwICu9". You can then add that context_uri to correspond with an NFC tag in [nfc_spot.json](./data/nfc_spot.json).
- If you are like me and are doing this for many albums and playlists I have a Python script **link_uri_conversion.py** to help. First put all the Spotify share links in the file [spotify_links.txt](./data/spotify_links.txt). Then run the script to convert all the links to the context_uri format.
- The Spotify API [Start/Resume Playback endpoint](https://developer.spotify.com/console/put-play/) appears to only be able to play albums, playlists, shows, and artists. If you want to play an individual song you would need to play it from an album or playlist. If you wanted to play a specific podcast episode you would need to do that from a show. There is an offset field to help with that. Check the example [nfc_spot.json](./data/nfc_spot.json) above to better understand the offset options.

### Coaster Setup
- If you decided to use coasters for this project here is the [youtube](https://www.youtube.com/watch?v=RV7-3CawKAM&t=68s&ab_channel=DIYPETE) tutorial I followed.
- In his tutorial he used felt pads on the bottom, I opted for a [cork backing](https://www.amazon.com/gp/product/B0834MWWS8/). There is probably a better way to do this, but I used an X-acto knife to cut away a small cavity for the NFC tag to sit. I then hot glued the cork backing to the coaster such that you couldn't see the NFC tag.
- I also printed out my album covers and playlist covers at Walmart as 4x6 prints. I included a Python script **convert_album_cover.py** to help convert square images to fit in 4x6 prints assuming you are using 4 inch tiles. First crop all your images so they are squares then put all images in the [albumart/originalcover](./albumart/originalcover) directory. Run the **convert_album_cover.py** script and the 4x6 formatted prints will be put in the [albumart/4x6prints](./albumart/4x6prints) directory.

## Usage

- To test this out and verify everything is working correctly run the Python script **spotifycoasters.py**.
- Once everything is working correctly there are a few more steps to set this up to run in the background on startup on a Windows machine.
    - In **spotifycoasters.py** there should be a line of code commented out running the function os.chdir. Uncomment that function and enter in the complete path to the directory of this script. You may need to escape backslashes in your path.
    - In **spotifycoasters.bat** replace the path with the complete path to the **spotifycoasters.py** file.
    - In **spotifycoasters.vbs** replace the path with the complete path to the **spotifycoasters.bat** file.
    - Open the Registry Editor and navigate to "Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    - Right click and select new and then select string value. Name this whatever you like.
    - Right click this new item and select modify. Enter in the complete path to the **spotifycoasters.vbs** file.
    - Now when you restart your computer the **spotifycoasters.py** script will be running in the background.

## Credits

[Automate Spotify with Python (Spotify API) - Euan Morgan](https://www.youtube.com/watch?v=-FsFT6OwE1A&t=450s&ab_channel=EuanMorgan) was extremely helpful in understanding the Spotify API.

[How to Make Coasters - DIY Gift Ideas - DIY PETE](https://www.youtube.com/watch?v=RV7-3CawKAM&t=68s&ab_channel=DIYPETE) was helpful for learning how to make custom coasters

[Python Automation project : Run Python scripts Automatically in backgroud on windows startup - Code Bear](https://www.youtube.com/watch?v=XWV9tatoPQI&ab_channel=CodeBear) was helpful in understanding how to run this script on startup.


## License

No License for now until I have a better understanding of this. Would like this to be free for non commercial use.
