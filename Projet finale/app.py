from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

#Create an instance of Flask
app = Flask(__name__)

#Create an instance of MySQL
mysql = MySQL()

#Create an instance of Flask RESTful API
api = Api(app)

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ArouneKr'
app.config['MYSQL_DATABASE_PORT'] = '3306'
app.config['MYSQL_DATABASE_DB'] = 'Orpi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#Initialize the MySQL extension
mysql.init_app(app)


#Get All Users, or Create a new user
class UserList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from orpi.maisons""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _type = request.form['type']
            _prix = request.form['prix']
            _ville = request.form['ville']
            insert_user_cmd = """INSERT INTO orpi.maisons(type, prix, ville) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_type, _prix, _ville))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
            
#Get a user by id, update or delete user
class User(Resource):
    def get(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from oorpi.maisons where id = %s',user_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _type = request.form['type']
            _prix = request.form['prix']
            _ville = request.form['ville']
            update_user_cmd = """update orpi.maisons 
                                 set type=%s, prix=%s, ville=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_type, _prix, _ville, user_id))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from orpi.maisons where id = %s',user_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

#API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:user_id>', endpoint='user')

if __name__ == "__main__":
    app.run(debug=True)