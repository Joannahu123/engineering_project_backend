from flask import Flask, jsonify, request
from flask_cors import CORS
from __init__ import db, app

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# add an api endpoint to flask app
@app.route('/bailey')
def get_bailey():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Bailey",
        "LastName": "Leeder",
        "DOB": "June 7",
        "Residence": "San Diego",
        "Email": "baileyleeder101@gmail.com",
        "Owns_Cars": ["none"]
    })

    return jsonify(InfoDb)

#lalita
@app.route('/lalita')
def get_lalita():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Lalita",
        "LastName": "Narayanan",
        "DOB": "September 18",
        "Residence": "San Diego",
        "Email": "lalitan34221@stu.powayusd.com",
        "Owns_Cars": ["none"]
    })

    return jsonify(InfoDb)

#joanna
@app.route('/joanna')
def get_joanna():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Joanna",
        "LastName": "Hu",
        "DOB": "April 26",
        "Residence": "San Diego",
        "Email": "joanna.y.hu@gmail.com",
        "Owns_Cars": ["none"]
    })

    return jsonify(InfoDb)

#yuva
@app.route('/yuva')
def get_yuva():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Yuva",
        "LastName": "Bala",
        "DOB": "Feburary 14",
        "Residence": "San Diego",
        "Email": "yuvabala214@gmail.com",
        "Owns_Cars": ["Tesla-Model-3", "Tesla-Model-X", "Cybertruck"]
    })

    return jsonify(InfoDb)

#ahmad
@app.route('/ahmad')
def get_ahmad():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Ahmad",
        "LastName": "Imran",
        "DOB": "May 28",
        "Residence": "San Diego",
        "Email": "ahmadimran.2009@outlook.ie",
        "Owns_Cars": ["none"]
    })

    return jsonify(InfoDb)

#nathan 
@app.route('/nathan')
def get_nathan():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Nathan",
        "LastName": "Tejidor",
        "DOB": "October 7",
        "Residence": "San Diego",
        "Email": "nateji5@gmail.com",
        "Owns_Cars": ["none"]
    })

    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)