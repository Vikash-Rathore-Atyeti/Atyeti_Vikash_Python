from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db_config import get_connection
from typing import List

app_fastapi=FastAPI()

# model for user
class User(BaseModel):
    id:int
    name:str
    email:str


@app_fastapi.get("/users",response_model=List[User])
def getUsers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

@app_fastapi.get('/user/{user_id}',response_model=User)
def getUserById(user_id:int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * from users where id=%s',(user_id))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return user
    else:
        raise HTTPException(status_code= 404,detail="user not found")

@app_fastapi.delete('/delete/{user_id}')
def deleteUserById(user_id):
    conn=get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("delete from users where id=%s",(user_id))
    cursor.close()
    conn.close()

    return {"message":f"user id {user_id} has been deleted succesfully"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app_fastapi,host="0.0.0.0",port=9000)