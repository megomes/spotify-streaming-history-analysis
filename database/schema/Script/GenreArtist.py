from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def saveGenreArtist(genre_artist):
    code = RAMData.getCode(genre_artist)
    genre_artist_id = RAMData.instance().genre_artist.get(code)
    if genre_artist_id is not None:
        return

    genre_artist['genre_artist_id'] = SQLConn.instance().getId('genre_artist')
    SQLData.instance().insert_genre_artist(genre_artist)
    RAMData.instance().genre_artist[code] = genre_artist['genre_artist_id']