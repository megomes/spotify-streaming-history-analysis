from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def savePlay(play):
    code = RAMData.getCode(play)
    play_id = RAMData.instance().play.get(code)
    if play_id is not None:
        return

    play['play_id'] = SQLConn.instance().getId('play')
    SQLData.instance().insert_play(play)
    RAMData.instance().play[code] = play['play_id']