# FUNCTION BASED REST API USING FLASK

from flask import Flask,request,jsonify
from db_config import get_connection

app = Flask(__name__)
conn = get_connection()
cursor =conn.cursor(dictionary=True)

@app.route('/users',methods=['GET'])
def get_users():

    #A dictionary, where you access values by column name
    cursor.execute("select * from users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    cursor.execute("select * from users where id=%s",(user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify(user)
    else:
        return jsonify({"error":"User not found"}),404


@app.route('/delete/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("delete from users where id=%s",(user_id,))
    conn.commit()

@app.route('/update/<int:user_id>/<name>/', methods=['PATCH'])
def update_user_by_id(user_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"User {user_id} updated to name '{name}'"})



if __name__ == '__main__':
    app.run(debug=True)
