import time
import struct
import urllib.parse, urllib.request
import csv

def construct_request_body(timestamp, itunes_identifier):
    hex = "61 6a 43 41 00 00 00 45 6d 73 74 63 00 00 00 04 55 94 17 a3 6d 6c 69 64 00 00 00 04 00 00 00 00 6d 75 73 72 00 00 00 04 00 00 00 81 6d 69 6b 64 00 00 00 01 02 6d 69 64 61 00 00 00 10 61 65 41 69 00 00 00 08 00 00 00 00 11 8c d9 2c 00"

    body = bytearray.fromhex(hex);
    body[16:20] = struct.pack('>I', timestamp)
    body[-5:] = struct.pack('>I', itunes_identifier)
    return body


def add_song(itunes_identifier, myvars):
    data = construct_request_body(int(time.time()), itunes_identifier)
    XDsid, Cookie, XGuid = myvars['XDsid'], myvars['Cookie'], myvars['XGuid']

    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0",
        "Client-iTunes-Sharing-Version" : "3.12",
        "Accept-Language" : "nl-nl, nl;q=0.83, fr-fr;q=0.67, fr;q=0.50, en-us;q=0.33, en;q=0.17",
        "Client-Cloud-DAAP-Version" : "1.0/iTunes-12.2.0.145",
        "Accept-Encoding" : "gzip",
        "X-Apple-itre" : "0",
        "Client-DAAP-Version" : "3.13",
        "User-Agent" : "iTunes/12.3.2 (Macintosh; OS X 10.11.2) AppleWebKit/601.3.9",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-dmap-tagged",
        # Replace the values of the next three headers with the values you intercepted
        "X-Dsid" : XDsid,
        "Cookie" : Cookie,
        "X-Guid" : XGuid,
        "Content-Length" : "77"
    }

    request = urllib.request.Request("https://ld-4.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/cloud-add", data, headers)
    urllib.request.urlopen(request)

# Some code to read variables used in the add_song function (you'll need to use an https proxy such as Charles to figure out what yours might be
with open("setup-applemusic.txt") as myfile:
    myvars = {k: v.strip() for k, v in [line.split(':') for line in myfile]}


with open('itunes.csv') as itunes_identifiers_file:
    itunes_reader = csv.reader(itunes_identifiers_file)
    next(itunes_reader)

    for row in itunes_reader:
        itunes_identifier = int(row[0])
        title, artist, album = row[1], row[2], row[3]

        try:
            add_song(itunes_identifier, myvars)
            print("Successfuly added song {}, by {}, on album {} to your Library.".format(title, artist, album))
            # Try playing with the interval here to circumvent the API rate limit; 10 seems to work fine on mine
            time.sleep(10)
        except Exception as e:
            print("Something went wrong while adding song {} with ID {} to your Library. The error: {}.".format(title, str(itunes_identifier), str(e)))
