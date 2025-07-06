import psycopg2
import psycopg2.extras

class SQLConn:
    __instance = None
    cursor = None
    conn = None

    ids = {
        'album': 0,
        'artist': 0,
        'music': 0,
        'genre': 0,
        'category': 0,
        'genre_category': 0,
        'music_artist': 0,
        'album_music': 0,
        'genre_artist': 0,
        'play': 0,
        'favorite': 0,
        
    }

    @staticmethod
    def instance():
        if not SQLConn.__instance:
            SQLConn.__instance = SQLConn()
        return SQLConn.__instance

    def __init__(self):
        # Connect
        self.conn = psycopg2.connect(user='postgres', database="postgres", password='password', host='localhost', port='5432')
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def getId(self, table):
        self.ids[table] = self.ids[table] + 1
        return self.ids[table]