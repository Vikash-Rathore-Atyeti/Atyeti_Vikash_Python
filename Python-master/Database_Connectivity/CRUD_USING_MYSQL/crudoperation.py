from db_config import getConnection

def getUsers():
    conn=getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for i in users:
        print(i)


def updateUser():
    conn=getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("update users set name='akshay' where id=1")
    conn.commit()
    cursor.close()
    conn.close()



if __name__=='__main__':
    getUsers()
    updateUser()