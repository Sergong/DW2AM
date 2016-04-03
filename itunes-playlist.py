###############################################################################
#
# File:         itunes-playlist.py
# RCS:          $Header: $
# Description:  Interact with iTunes
# Author:       Serge Meeuwsen, Jim Randell
# Created:      Mon Jan 18 2016
# Modified:     Sun Apr 3 2016
# Parts:     Sat Oct 20 17:19:04 2012 (Jim Randell) jim.randell@gmail.com
# Language:     Python
# Package:      N/A
# Status:       Experimental (Do Not Distribute)
#
# (C) Copyright 2009, Jim Randell, all rights reserved.
# (C) Copyright 2016, Serge Meeuwsen, all rights reserved.
#
###############################################################################

import appscript
import sys
import csv


def find_track(allsongs, name, artist, album):
    print("Searching for song {}, by {}...".format(name, artist))
    for song in allsongs:
        if (song.name().lower() == name.lower() or name.lower() in song.name().lower()) and (album.lower() in song.album().lower() or song.album().lower() in album.lower() ):
            return song


def new_playlist(name):
    "new-playlist <playlist> - Creates a Playlist from the added tracks on todays date"
    app = appscript.app('iTunes')
    # create a playlist with the chosen name
    print("Creating iTunes playlist: %s" % name)
    playlist = app.make(new=appscript.k.playlist)
    playlist.name.set(name)
    new_playlist = playlist
    allsongs = app.library_playlists['Library'].tracks()
    with open('itunes.csv', encoding='utf-8') as playlist_file:
        playlist_reader = csv.reader(playlist_file)
        next(playlist_reader) # Skip the header
        for row in playlist_reader:
            title, artist, album = row[1], row[2], row[3]
            track = find_track(allsongs, title, artist, album)
            if track:
                # print("Found song {}, by {}, on album {}! Adding to playlist.".format(title, artist, album))
                app.duplicate(track, to=new_playlist)
            else:
                print("Couldn't find song {}, by {}, on album {}!".format(title, artist, album))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        new_playlist(sys.argv[1])
    else:
        print("Please provide a playlistname. Exitting...")


