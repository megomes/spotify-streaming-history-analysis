from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveFavorite(favorite):
    code = RAMData.getCode(favorite)
    favorite_id = RAMData.instance().favorite.get(code)
    if favorite_id is not None:
        return

    favorite['favorite_id'] = SQLConn.instance().getId('favorite')
    SQLData.instance().insert_favorite(favorite)
    RAMData.instance().favorite[code] = favorite['favorite_id']