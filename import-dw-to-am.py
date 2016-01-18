#
#
#  Master script to call individual scripts
#
#
import os
import datetime

os.system('python3 export-dw-playlist.py')
os.system('python3 retrieve-identifiers.py')
os.system('python3 insert-songs.py')

WEEKLY_PLAYLIST_NAME = "Discover_Weekly_{}".format("_".join(str(v) for v in datetime.date.today().isocalendar()[:2]))
print("Executing: python3 itunes.py new_playlist " + WEEKLY_PLAYLIST_NAME)
os.system("python3 itunes-playlist.py " + WEEKLY_PLAYLIST_NAME)
