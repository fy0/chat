# coding:utf-8

#class sessionBackend(dict):
#    pass

#sessiondata = sessionBackend()

sessiondata = dict()

class Session:
    def __init__(self,_uuid):
        if not _uuid in sessiondata:
            sessiondata[_uuid] = {}
        self.data = sessiondata[_uuid]
    def __getitem__(self,key):
        return self.data.get(key,None)
    def __setitem__(self,key,value):
        self.data[key] = value

