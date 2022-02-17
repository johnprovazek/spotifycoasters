with open('../data/spotify_links.txt') as spotify_links:
    for link in spotify_links:
        link_split = link[25:].split("/")
        formatted_uri = "spotify:" + link_split[0] + ":" + link_split[1][0:22]
        print(formatted_uri)