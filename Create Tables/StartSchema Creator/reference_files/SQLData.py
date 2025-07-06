from Script.SQLConn import SQLConn
from Script.RAMData import RAMData

import sys

import uuid

class SQLData:
    __instance = None

    $declarations

    @staticmethod
    def instance():
        if not SQLData.__instance:
            SQLData.__instance = SQLData()
        return SQLData.__instance

    def checkMaxSize(self):
        if len(self.$main_table) >= 1000:
            # time to save on db!
            self.save()
            return True
        return False

    def save(self):
        $save


    #############################
    # INSERT

$insert

    #############################
    # SAVE

$query