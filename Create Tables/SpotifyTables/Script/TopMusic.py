from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveTopMusic(top_music):
    code = RAMData.getCode(top_music)
    top_music_id = RAMData.instance().top_music.get(code)
    if top_music_id is not None:
        return

    top_music['top_music_id'] = SQLConn.instance().getId('top_music')
    SQLData.instance().insert_top_music(top_music)
    RAMData.instance().top_music[code] = top_music['top_music_id']