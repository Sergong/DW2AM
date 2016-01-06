#
#
#  Master script to call individual scripts
#
#
import os
import datetime
# import sys                                            -- Version 1

# url = sys.argv[1:][0]                                 -- Version 1

# os.system('python3 write-spotify-csv.py ' + url)      -- Version 1
os.system('python3 export-dw-playlist.py')           #  -- Version 2 addition
os.system('python3 retrieve-identifiers.py')
os.system('python3 insert-songs.py')

WEEKLY_PLAYLIST_NAME = "Discover_Weekly_{}".format("_".join(str(v) for v in datetime.date.today().isocalendar()[:2])) #  -- Version 2 addition

os.system("python3 itunes.py new_playlist " + WEEKLY_PLAYLIST_NAME)  #  -- Version 2 addition