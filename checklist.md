# Pre-checklist install
installing pipenv on a global scope


`!Only needs to be done once!`

```console
pip install pipenv
``` 

# Start of checklist
- Create a folder for our new assignment
- go into that folder
- create the virtual env with flask

```console
pipenv install flask PyMySQL
```
- WARNING! Make sure pipfile & pipfile.lock are there!! If not FIX THIS NOW!!!
- activate virtual env
```console
pipenv shell
```

---
- Create folder structure
```
- flask_app(📂)
    - config (📂)
        - mysqlconnection.py(📜)
    - controllers (📂)
        # You will have a controller file for every table table in your database
        -controller_user.py(📜)
    - models (📂)
        # You will have a model file for every table in your database
        model_user.py(📜)
    - static (📂)
        - css(📂)
            - styles.css (📃)
        - img (📁)
        - js(📂)
            - script.js (📃)
    - templates (📂)
        - user.html (📄)
    - __init__.py (📜)
- pipfile(📄)
- pipfile.lock(📄)
- server.py(📜)
```

## Create server.py

```Py
from flask_app import app

#TODO import controllers

#MAKE SURE THIS IS AT THE BOTTOM
if __name__=="__main__":
    app.run(debug=True)
```
- Create templates folder
- add user.html in templates folder
- Test it out

## Create mysqlconnection.py file

```PY
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
```

## create model file
- change this file based on your table in db
    - each model has its own controller
```PY
# import the function that will return an instance of a connection
#       folder  folder  file                    function
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the users table from  database
class User:
    # should change db based on schema you're trying to access
    DB = 'users_db'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f'{self.first_name} {self.last_name}'
        
    #TODO CREATE
    #* the save method will be used when we need to save a new user to our database
    @classmethod
    def create(cls, data):
        """
        This if successful add user to database and returns the new row's id
        """
        query = """INSERT INTO users (first_name, last_name, email)
                VALUES (%(first_name)s, %(last_name)s,%(email)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    #TODO READ
    #*the display_all_users method will be used when we need to retrieve all the rows of the table user
    @classmethod
    def get_all(cls):
        """
        Function doesn't take in anything but returns a list of instances of dealers
        """
        query = """SELECT * FROM users;"""
        #what is results?  list !! list of what? dictionaries
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        #transform the list of dictionaries -> a list of object/instances
        for dict in results:
            users.append(cls(dict))
        return users
    
    #* the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls,data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        # data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
    
    
    #TODO UPDATE
    #* the update method will be used when we need to update a user in our database
    @classmethod
    def update(cls,data):
        query = """UPDATE users 
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    #TODO DELETE
    #* the delete method will be used when we need to delete a user from our database
    @classmethod
    def delete(cls,data):
        """
        This function takes in a dictionary containing a key of 'id' and value that is the int representation of the id you want to delete
        """
        query = """DELETE FROM users WHERE id = %(id)s;"""
        # data = {'id': id}
        #returns nothing
        return connectToMySQL(cls.DB).query_db(query,data)
```

## create controller.py file
- each controller has its own model
    - don't forget to import models
```PY
from flask_app import app
from flask import render_template, request, redirect, session

from flask_app.models.model_user import User

#THIS WILL MOVE

@app.route('/')
def index():
    return redirect('/users')

#READ
@app.route('/users')
def display_users():
    # calling to 
    all_users = User.get_all()
    # passing all users to our template so we can display them there
    return render_template("display_users.html", users = all_users)

#CREATE
@app.route('/users/create', methods=['POST'])
def create():
    User.create(request.form)
    return redirect('/users')

@app.route('/users/new')
def create_users():
    return render_template('create_user.html')

@app.route('/users/show/<int:id>')
def display_user(id):
    data = {
        'id' : id
    }
    user = User.get_one(data)
    return render_template('display_user.html', user = user)

#update
@app.route('/users/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/users')


@app.route('/users/edit/<int:id>')
def update_user(id):
    data = {
        'id' : id
    }
    user= User.get_one(data)
    return render_template('update_user.html', user = user)

#delete
@app.route('/users/delete/<int:id>')
def delete(id):
    data = {
        'id' : id
    }
    User.delete(data)
    return redirect('/users')

```

## create  \_\_init__.py file
```PY
from flask import Flask
#app = instance of Flask(class)
app = Flask(__name__)
app.secret_key = "do not forget to add secret key"
```