from flask import Flask , render_template , url_for , redirect , request , session
from flask import Flask, jsonify, request, json

from flask import send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime


app = Flask( __name__ )
# app = Flask(__name__, static_folder='./build',static_url_path='/')
from sqlalchemy import create_engine

DB_URL = 'postgres://ugcuvkvpcdaixu:b624b6193c9e248af602f7239c6ddca6848239242adbcb31a9fd4685ac75aabf@ec2-204-236-228-169.compute-1.amazonaws.com:5432/d93me5889f2sp1'
engine = create_engine(DB_URL)
connection = engine.connect()

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy( app )
bcrypt = Bcrypt(app)

# route decorator to end point to application
# endpoint anything the starts with /
#cbecks the endpoint of the path and routes there
# @app.route( '/' , methods=[ 'GET' , 'POST' ] )
# def index( ) :
#     # function to handle the request to a endpoint
#     # shows output convincing the developer that the server is running
#     # rendering the home page which is index.html
#     # fruits = [ 'Apple' , 'Orange' ]
#     # database addition
#     cur = mysql.connection.cursor( )
#     # cur.execute( "INSERT INTO user VALUES(%s)" , [ 'Mike' ] )
#     # mysql.connection.commit()
#     # result_value = cur.execute("SELECT * FROM user")
#     # if result_value > 0 :
#     #     users = cur.fetchall( )
#     #     print(users,type(users))
#     #     return users[ 0 ][ 0 ]
#     if cur.execute( "INSERT INTO user(user_name) VALUES ('Ben')" ) :
#         mysql.connection.commit( )
#         return 'success' , 201
#     if request.method == 'POST' :
#         return request.form[ 'password' ]
#     return render_template( 'index.html' )#, fruits = fruits )
#     # redirect the homepage to the about page
#     #  return redirect( url_for( 'about' ) )

# @app.route( '/' , methods = [ 'GET' , 'POST' ] )
# @app.route( '/' )
#def index(  ) :
    #return send_from_directory('./src', '/index.js')
    # return app.send_static_file( 'index.html' )
    # if request.method == 'POST' :
    #     form = request.form
    #     nm = form[ 'name' ]
    #     unm = form[ 'username' ]
    #     # pw = form[ 'password' ]
    #     # age = form[ 'age' ]
    #     ids = len( connection.execute( 'SELECT * FROM users;' ).fetchall( ) )
    #     # connection.execute( 'INSERT INTO users(id,name,username) VALUES(1, name,username);' , ( name0 , username0 ) )
    #     connection.execute( "INSERT INTO users(id,name,username,password) VALUES(%s,%s,%s,%s)" , ( ids+1 , nm , unm , "Pass@1" ) )
    #     # connection.execute('INSERT INTO users(id,name,username) VALUES(1,'Isaiah','Sherfick');')
    #     # connection.commit( )
    #     # db.connection.commit( )
    #     return "success"
    # return app.send_static_file('index.html')

CORS(app)

@app.route('/users/register', methods=['GET','POST'])
def register():
    first_name = request.get_json()['name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    ids = len( connection.execute( 'SELECT * FROM users;' ).fetchall( ) )
    connection.execute( 'INSERT INTO users(id,name,username,password) VALUES(%s,%s,%s,%s);' , ( ids+1, first_name,email,password ) )
    result = {'email': email + ' registered'}
    return jsonify({'result' : result})

@app.route('/users/login', methods=['POST'])
def login():
    #users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({'token':access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})
    else:
        result = jsonify({"result":"No results found"})
    return result

@app.route( '/employees' )
def employees( ) :
    cur = mysql.connection.cursor( )
    result_value = cur.execute( "SELECT * FROM employee" )
    if result_value > 0 :
        employees = cur.fetchall( )
        return render_template( 'employees.html' , employees = employees )

@app.errorhandler( 404 )
def page_not_found( e ) :
    return 'This page was not found'

# route to the about page
@app.route( '/about' )
def about( ) :
    # rendering the about html page and returning it
    return render_template( 'about.html' )

# #route to css
# @app.route( '/css' )
# def css( ) :
#     # rendering the css page
#     return render_template( 'css.html' )

# checks whether current file is running
if __name__ == '__main__' :
    # debug = True makes it convenient by restarting the server whenever code is updated
    # default port 5000 , can pass it in the argument if we want to change it
    app.run( debug = True , port = 5000 )
 
