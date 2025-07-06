%load_ext autoreload
%autoreload 2

from Script import Album, Artist, Music, Genre, Category, GenreCategory, MusicArtist, AlbumMusic, GenreArtist, Play, Favorite
from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

## Postgres

# Connect to Database
print('Connecting to the Database...')
SQLConn.instance()

# Erase all tables
SQLConn.instance().cursor.execute("DROP TABLE IF EXISTS album,artist,music,genre,category,genre_category,music_artist,album_music,genre_artist,play,favorite CASCADE;")

# Create tables
sql_createtables_string = open('create_tables.sql', 'r', encoding="utf-8").read()
SQLConn.instance().cursor.execute(sql_createtables_string)

# RAM Started
ramData = RAMData.instance()

# SQL Started
sqlData = SQLData.instance()

# Commit and create Tables
SQLConn.instance().conn.commit()
print('Connected!')

##############################
# PROCESS CODE
##############################

# Save everything else remaining
sqlData.save()

## Commit changes
SQLConn.instance().conn.commit()
print('Done!')