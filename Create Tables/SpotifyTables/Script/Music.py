from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def getMusicId(music):
    music_id = RAMData.instance().music.get(music['title'])
    if music_id is not None:
        return music_id

    music['music_id'] = SQLConn.instance().getId('music')
    SQLData.instance().insert_music(music)
    RAMData.instance().music[music['title']] = music['music_id']
    return music['music_id']

def updateMusic(music):
    SQLData.instance().update_music(music)
