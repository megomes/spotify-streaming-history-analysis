from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveGenreCategory(genre_category):
    code = RAMData.getCode(genre_category)
    genre_category_id = RAMData.instance().genre_category.get(code)
    if genre_category_id is not None:
        return

    genre_category['genre_category_id'] = SQLConn.instance().getId('genre_category')
    SQLData.instance().insert_genre_category(genre_category)
    RAMData.instance().genre_category[code] = genre_category['genre_category_id']