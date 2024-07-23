"""link_uri_conversion.py converts a text file of Spotify share links to Spotify URIs. """

# This script takes in a text file containing Spotify share links and outputs the corresponding spotify URIs.
#
# Example: [python link_uri_conversion.py ../links.txt]

import sys  # Used to handle command line arguments.


# Command line arguments.
links = sys.argv[1]

# Converting Spotify share links to URIs.
with open(links, encoding="utf-8") as spotify_links:
    for link in spotify_links:
        link_split = link[25:].split("/")
        formatted_uri = "spotify:" + link_split[0] + ":" + link_split[1][0:22]
        print(formatted_uri)
