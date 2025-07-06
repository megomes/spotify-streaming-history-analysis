from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def getGenreId(genre):
    genre_id = RAMData.instance().genre.get(genre['genre'])
    if genre_id is not None:
        return genre_id

    genre['genre_id'] = SQLConn.instance().getId('genre')
    SQLData.instance().insert_genre(genre)
    RAMData.instance().genre[genre['genre']] = genre['genre_id']
    return genre['genre_id']

def updateGenre(genre):
    SQLData.instance().update_genre(genre)
