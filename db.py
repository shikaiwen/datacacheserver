# coding:utf-8
import sqlite3
import os

class DB(object):
    
    def createTable(self):
        self.exesql("create table datacache(url text, content text )")
    
    def getconn(self):
        conn = sqlite3.connect(os.path.dirname(__file__) +"/cache.db")
        return conn
    
    
    def getcursor(self):
        conn = self.getconn()
        c = conn.cursor()
        return c
    
    def exesql(self, sql, datalist):
        conn = self.getconn()
        c = conn.cursor()
        c.execute(sql, datalist)
        conn.commit()
        conn.close()
        
    def getdatabyurl(self, url):
        conn = self.getconn()
        c = conn.cursor()
        
        c.execute("select * from datacache where url = ?", [url])
        res = c.fetchone()
        
        conn.commit()
        
        conn.close()
        return res
        





    
