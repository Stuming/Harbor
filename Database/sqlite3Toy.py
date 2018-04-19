# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 20:08:45 2018

@author: Stuming
"""

import sqlite3 as db


def insertdata():
    # the first method to insert data
    cursor.execute("""INSERT INTO orders VALUES (
            'A0001', '2013-12-01', 'AAPL', 1000, 203.4)""")
    
    # the second method to insert data
    orders = [('A0002', '2013-12-02', 'MSFT', 1500, 167.5), 
              ('A0003', '2013-12-02', 'GOOG', 1500, 167.5)]
    cursor.executemany("""INSERT INTO orders VALUES(?, ?, ?, ?, ?)""", orders)
    
    connection.commit()
    
    
def querydata():
    cursor.execute("""SELECT * from orders 
                   where symbol='AAPL' order by quantity""")
    for row in cursor:
        print(row)
    
    stock = 'MSFT'
    cursor.execute("""SELECT * FROM orders 
                   where symbol=? order by quantity""", (stock,))
    print(cursor.fetchall())
    
    
if __name__ == '__main__':
    connection = db.connect('LearningMysql')
    cursor = connection.cursor()
    cursor.execute(("""CREATE TABLE IF NOT EXISTS orders(
            order_id TEXT PRIMARY KEY,
            data TEXT,
            symbol TEXT,
            quantity INTEGER,
            price NUMBER)"""))
    
    # insertdata()
    querydata()
    
    cursor.close()
    connection.close()
    