from SQLConn import SQLConn
from RAMData import RAMData

import sys

import uuid

class SQLData:
    __instance = None

    @staticmethod
    def instance():
        if not SQLData.__instance:
            SQLData.__instance = SQLData()
        return SQLData.__instance