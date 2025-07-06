from SQLConn import SQLConn

class RAMData:
    __instance = None

    music = {}

    @staticmethod
    def instance():
        if not RAMData.__instance:
            RAMData.__instance = RAMData()
        return RAMData.__instance

    def __init__(self):
        sqlconn = SQLConn.instance()