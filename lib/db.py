#!/usr/bin/python
# -*- coding: utf-8 -*-

# lib/db.py
# -----------------------
# This represents the database where the data will be logged.
# Its a collection of SQLite3 objects wrapped together for ease.


import sqlite3
import os
import sys


class dbObjectBase(object):
    '''
    Base dbObject:
        This represents the database where the data will be logged. 
        Its a collection of SQLite3 objects wrapped together for ease.
        This base holds internal code for the class.
        
        if dbPath is left blank on initialisation it will use an in
        :memory: database
    '''
    connection = sqlite3.Connection
    cursor = sqlite3.Cursor
    dbPath = ''
    dataTableName = ''
    
    def __init__(self, dbPath=':memory:', dataTableName='data'):
        self.dbPath = dbPath
        self.dataTableName = dataTableName
        self.connection = sqlite3.connect(self.dbPath)
        self.cursor = self.connection.cursor()
        self._checkDB()        
        
    def _checkDB(self):      
        sSQL = 'SELECT count(*) FROM sqlite_master WHERE type="table" AND name=?;'
        self.cursor.execute(sSQL, (self.dataTableName,))
        ret = self.cursor.fetchone()
        if ret[0] == 0:
            self._createDB()        
            
    def _createDB(self):
        sSQL = 'CREATE TABLE ' + self.dataTableName + '(id INTEGER PRIMARY KEY, datetime REAL, name TEXT, ipAddress TEXT, fieldName TEXT, value REAL);'
        self.cursor.execute(sSQL)
            
    def test(self):
        sSQL = 'SELECT * from ' + self.dataTableName + ';'
        self.cursor.execute(sSQL)
        ret = self.cursor.fetchall()
        for row in ret:
            print row             
        
class dbObject(dbObjectBase):
    '''
    dbObject:
        This represents the database where the data will be logged. 
        Its a collection of SQLite3 objects wrapped together for ease.
        
        if dbPath is left blank on initialisation it will use an in
        :memory: database
    '''
    
    def _prepareData(self, data):
        ret = ''
        return fields + values
    
    def insertData(self, table, fields, values):
        '''Inserts data into database'''
        pass
            
            
if __name__ == '__main__':
    pass