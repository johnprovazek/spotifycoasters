import sys # Used to handle command line arguments

# Usage: This script is used to take in a text file containing spotify share links 
#        and output the corresponding spotify uri. Use these spotify uris in your
#        nfc_spot.json file.
# Example run: "python link_uri_conversion.py ../links.txt"

# Command line arguments
links = sys.argv[1]

# Coverting share links to uri
with open(links) as spotify_links:
    for link in spotify_links:
        link_split = link[25:].split("/")
        formatted_uri = "spotify:" + link_split[0] + ":" + link_split[1][0:22]
        print(formatted_uri)