from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveAlbumArtist(album_artist):
    code = RAMData.getCode(album_artist)
    album_artist_id = RAMData.instance().album_artist.get(code)
    if album_artist_id is not None:
        return

    album_artist['album_artist_id'] = SQLConn.instance().getId('album_artist')
    SQLData.instance().insert_album_artist(album_artist)
    RAMData.instance().album_artist[code] = album_artist['album_artist_id']