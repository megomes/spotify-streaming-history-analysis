from Script.SQLConn import SQLConn

class RAMData:
    __instance = None

    $declarations

    @staticmethod
    def instance():
        if not RAMData.__instance:
            RAMData.__instance = RAMData()
        return RAMData.__instance

    def __init__(self):
        sqlconn = SQLConn.instance()

    @staticmethod
    def getCode(item):
        code_arr = []
        for key in item.keys():
            code_arr.append(str(item[key]))
        return '+'.join(code_arr)