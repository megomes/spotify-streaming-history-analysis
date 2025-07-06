from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def getArtistId(artist):
    artist_id = RAMData.instance().artist.get(artist['title'])
    if artist_id is not None:
        return artist_id

    artist['artist_id'] = SQLConn.instance().getId('artist')
    SQLData.instance().insert_artist(artist)
    RAMData.instance().artist[artist['title']] = artist['artist_id']
    return artist['artist_id']

def updateArtist(artist):
    SQLData.instance().update_artist(artist)
