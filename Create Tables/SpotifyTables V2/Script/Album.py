from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def getAlbumId(album):
    album_id = RAMData.instance().album.get(album['album_spotify_uri'])
    if album_id is not None:
        return album_id

    album['album_id'] = SQLConn.instance().getId('album')
    SQLData.instance().insert_album(album)
    RAMData.instance().album[album['album_spotify_uri']] = album['album_id']
    return album['album_id']

def updateAlbum(album):
    SQLData.instance().update_album(album)
