#coding:utf-8

import os
import sqlite3

class EasyDB:
    #conn = sqlite3.Connection
    def __init__(self, filename, schema = None, **kwargs):
        exist = os.path.exists(filename)
        if not (exist or schema):
            raise Exception("The specified database file does not exist, and you haven't provided a schema")
        self.conn = sqlite3.connect(filename)
        if not exist:
            for table_name, fields in schema.items():
                query = "CREATE TABLE %s (%s)" % (table_name, ", ".join(fields))
                self.query(query)
            self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def query(self, *args, **kwargs):
        cursor = self.conn.cursor()
        result = cursor.execute(*args, **kwargs)
        ret = result.fetchall()
        return ret

    def commit(self):
        self.conn.commit()

class kvDB(EasyDB):
    def __init__(self,filename):
        if os.path.exists(filename):
            self.conn = sqlite3.connect(filename)    
        else:
            EasyDB.__init__(self,filename,{'data':['key TEXT primary key','value TEXT']})
    def __getitem__(self,key):
        ret = self.query('select value from data where key="%s"' % key)
        if ret:
            return eval(ret[0])
        return ret
    def __setitem__(self,key,value):
        return self.query('replace into data values("%s","%s")'%(key,value))

