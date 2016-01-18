###############################################################################
#
# File:         itunes-playlist.py
# RCS:          $Header: $
# Description:  Interact with iTunes
# Author:       Serge Meeuwsen, Jim Randell
# Created:      Mon Jan 18 2016
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
import time
import sys
import datetime

# separator for playlist folders
SEP = ' > '

# you could set this to os.path.expanduser("~/Music/iTunes/iTunes Music/")
# if you haven't changed your library from the default, and that will save time
# especially if your library is large
MUSIC_LIBRARY = '/Volumes/iTunes/Library/Music/'


def playlist_path(playlist):
    "playlist_path - return the path of the playlist"

    path = []
    while True:
        path.insert(0, playlist.name())
        try:
            playlist = playlist.parent()
            kind = playlist.special_kind()  # this throws an error if the parent isn't really real
        except appscript.reference.CommandError:
            break

    return SEP.join(path)


def find_playlist(playlists, name, kind=appscript.k.none):
    "find_playlist - find a playlist in a list of playlists"

    # a number indicates a playlist index
    try:
        i = int(name)
    except ValueError:
        pass
    else:
        return playlists[i]

    # search for a playlist by path
    for playlist in playlists:
        if not playlist.special_kind() == kind: continue
        if playlist_path(playlist) == name: return playlist


def create_folder(app, path):
    "create_folder - return a playlist folder, creating folders as necessary"

    folder = find_playlist(app.playlists(), path, appscript.k.folder)
    if folder: return folder

    # split the path into parent and folder
    parts = path.rpartition(SEP)

    # create the folder
    print("Creating iTunes playlist folder: %s" % parts[2])
    folder = app.make(new=appscript.k.folder_playlist)
    folder.name.set(parts[2])

    # if there is a parent folder move it to there
    if parts[0]:
        parent = create_folder(app, parts[0])
        app.move(folder, to=parent)

    # return the newly created playlist
    return folder


def new_playlist(path):
    "new-playlist <playlist> - Creates a Playlist from the added tracks on todays date"

    # turn the playlist path into folder and name
    parts = path.rpartition(SEP)
    (folder, name) = (parts[0].rstrip(), parts[2].lstrip())

    app = appscript.app('iTunes')

    # create a playlist with the chosen name
    print("Creating iTunes playlist: %s" % name)
    playlist = app.make(new=appscript.k.playlist)
    playlist.name.set(name)

    # if there is a parent folder, find it (creating if necessary)
    if folder:
        parent = create_folder(app, folder)
        app.move(playlist, to=parent)

    new_playlist = playlist

    # add the tracks added today (possibly yesterday) to the new playlist
    for playlist in app.playlists():
        if playlist.name() == 'Recently Added':
            for track in playlist.tracks():
                cur_date = time.strftime("%Y-%m-%d")
                tdate = str(track.date_added())
                tdate = tdate.split(' ')[0]
                cdt = datetime.datetime.strptime(cur_date, "%Y-%m-%d")
                tdt = datetime.datetime.strptime(tdate, "%Y-%m-%d")
                datediff = int(str(cdt - tdt)[:1])
                print("Date Added: {}, Date Today: {}, Difference: {}".format(tdate, cur_date, str(datediff)))
                print("Date differs by {} days".format(datediff))
                if datediff == 0:
                    print("Adding track name: " + track.name())
                    app.duplicate(track, to=new_playlist)

    # show the playlist
    app.reveal(new_playlist)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        new_playlist(sys.argv[1])
    else:
        print("Please call with a playlist name...")
