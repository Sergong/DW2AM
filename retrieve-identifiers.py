import csv
import struct
import urllib.parse, urllib.request
import json


def retrieve_itunes_identifier(title, artist, album):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200"
    }
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(title + " " + artist)
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        # Attempt to match by title & artist
        for song in songs:
            if (song["name"].lower() in title.lower() or title.lower() in song["name"].lower()) and (song["artistName"].lower() in artist.lower() or artist.lower() in song["artistName"].lower()):
                return [song["id"], song["name"], song["artistName"], song["collectionName"]]
        # No match found, try album name
        for song in songs:
            if (album.lower() in song["collectionName"].lower() or song["collectionName"].lower() in album.lower()):
                return [song["id"], song["name"], song["artistName"], song["collectionName"]]
    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None


with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)
    # Open itunes.csv for writing the identifiers, along with the Title, Artist and Album as found on iTunes
    itunescsv = csv.writer(open('itunes.csv', 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    itunescsv.writerow(['identifier','title','artist','album'])

    for row in playlist_reader:
        title, artist, album = row[0], row[1], row[2]
        itunes_identifier = retrieve_itunes_identifier(title, artist, album)
        if itunes_identifier:
            print("{} - {} => {}".format(title, artist, itunes_identifier[0]))
            itunescsv.writerow([itunes_identifier[0],itunes_identifier[1],itunes_identifier[2],itunes_identifier[3]])
        else:
            print("{} - {} => Not Found".format(title, artist))