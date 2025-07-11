import psycopg2
import psycopg2.extras

class SQLConn:
    __instance = None
    cursor = None
    conn = None

    ids = {
        'musica': 0,
    }

    @staticmethod
    def instance():
        if not SQLConn.__instance:
            SQLConn.__instance = SQLConn()
        return SQLConn.__instance

    def __init__(self):
        # Connect
        self.conn = psycopg2.connect(user='postgres', database="postgres", password='123456', host='localhost', port='5432')
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def getId(self, table):
        self.ids[table] = self.ids[table] + 1
        return self.ids[table]