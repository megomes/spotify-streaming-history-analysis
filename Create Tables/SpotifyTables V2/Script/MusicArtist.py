from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveMusicArtist(music_artist):
    code = RAMData.getCode(music_artist)
    music_artist_id = RAMData.instance().music_artist.get(code)
    if music_artist_id is not None:
        return

    music_artist['music_artist_id'] = SQLConn.instance().getId('music_artist')
    SQLData.instance().insert_music_artist(music_artist)
    RAMData.instance().music_artist[code] = music_artist['music_artist_id']