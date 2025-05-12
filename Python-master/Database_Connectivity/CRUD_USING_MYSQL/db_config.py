import mysql.connector

def getConnection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='sampledb'
    )
