#
#
#  Master script to call individual scripts
#
#
import os
import datetime

os.system('python3 export-dw-playlist.py')

response = input('Would you like to import this playlist? (Y)es or any other key for No: ')
response = str(response)


if response.upper() == "Y":
    os.system('python3 retrieve-identifiers.py')
    os.system('python3 insert-songs.py')

    WEEKLY_PLAYLIST_NAME = "Discover_Weekly_{}".format("_".join(str(v) for v in datetime.date.today().isocalendar()[:2]))
    print("Songs added to the iTunes Library.")
    print("Now please execute the following to create the playlist in Apple Music: python3 itunes-playlist.py " + WEEKLY_PLAYLIST_NAME)
    #os.system("python3 itunes-playlist.py " + WEEKLY_PLAYLIST_NAME)

