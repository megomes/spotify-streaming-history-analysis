from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveAlbumMusic(album_music):
    code = RAMData.getCode(album_music)
    album_music_id = RAMData.instance().album_music.get(code)
    if album_music_id is not None:
        return

    album_music['album_music_id'] = SQLConn.instance().getId('album_music')
    SQLData.instance().insert_album_music(album_music)
    RAMData.instance().album_music[code] = album_music['album_music_id']