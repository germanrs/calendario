# -*- coding: utf-8 -*-
#
#Copyright (C) 2010-2012, Yader Velasquez
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
from os import path
import logging
import calendario

log = logging.getLogger('DataBase-Log')

class DataBase(object):
    """Connection to the database"""
    def __init__(self, db_path):
        create = False
        if not path.exists(db_path + '/data/calendario.db'):
            create = True
        
        self.connection = sqlite3.connect(db_path + '/data/calendario.db')
        self.cursor = self.connection.cursor()
        
        if create:
            self.cursor.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY \
                    AUTOINCREMENT, task TEXT NOT NULL, category INTEGER, \
                    priority INTEGER, completed INTEGER, date TEXT NOT \
                    NULL);")
    
    def add(self, data):
        '''Add a new row'''
        self.cursor.execute("INSERT INTO tasks VALUES (NULL,?,?,?,?,?);", data)
        self.connection.commit()

    def get(self, date):
        '''Get the rows acording to the date'''
        d = (date,)
        self.cursor.execute("SELECT * FROM tasks WHERE date=? ORDER BY completed asc, priority desc;", d)
        data = list()
        for i in self.cursor:
            task = calendario.Task(i[0], i[1], i[2], i[3], i[4])
            data.append(task)
        return  data

    def get_reminder(self):
        '''Get the tasks that needs be reminder'''
        self.cursor.execute("SELECT * FROM tasks WHERE completed=0 ORDER BY priority desc;")
        data = list()
        for i in self.cursor:
            task = calendario.Task(i[0], i[1], i[2], i[3], i[4])
            data.append(task)
        return  data

    def get_days(self, data):
        self.cursor.execute("SELECT substr(date, 1, 2) from tasks where substr(date, 4)=?;", data)
        data = list()
        for i in self.cursor:
            data.append(i[0])
        return data

    def filter_tasks(self, data):
        '''filter by category and priority'''
        self.cursor.execute("SELECT * FROM tasks WHERE date=? AND category=? AND priority=?", data)
        data = list()
        for i in self.cursor:
            task = calendario.Task(i[0], i[1], i[2], i[3], i[4])
            data.append(task)
        return  data

    def update(self, data):
        '''Update table'''
        #self.cursor.execute("UPDATE tasks SET task=?, category=?, priority=?, \
        #        completed=? where id=?; ", data)

        self.cursor.execute("UPDATE tasks SET completed=? where id=?;", data)
        self.connection.commit()

    def delete(self, data):
        '''Delete from database'''
        self.cursor.execute("DELETE FROM tasks WHERE id=?",data)
        self.connection.commit()

    def close(self):
        '''Close the connection'''
        self.cursor.close()
        self.connection.close()
