from pymongo import MongoClient

class Connect(object):
    @staticmethod
    def getConnection():
        return MongoClient('<<YOUR MONGO CONNECTION STRING HERE>>') #after that you can change this file name to "mongoConnectionFile.py"
