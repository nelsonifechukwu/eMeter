from app import app 
from flask import session, make_response, redirect, render_template, request, flash, url_for, Response
from flask_cors import cross_origin
from app.models import checklogin, get_transformer_data, insert_transformer_data, insert_transformer_input, get_transformer_input, delete_transformer_data
import json, random

API = 'xdol'

@app.route('/plot')
@cross_origin(origin='127.0.0.1', headers=['Content-Type', 'Authorization'])
def plot():
    #create a session to secure this endpoint
    """ user_name = session['username']
    if m_user != user_name: 
    """
    if "username" not in session:
        return redirect(url_for('login'))
    #data = get_transformer_data()
    return render_template('plot.html', name=session["username"]) #data = data

@app.route('/data', methods=['GET', 'POST'])
@cross_origin(origin='127.0.0.1', headers=['Content-Type', 'Authorization'])
def get_data():
    data = get_transformer_data()
    response = make_response(json.dumps(list(data)))
    response.content_type = 'application/json'
    return response

@app.route('/delete', methods = ('GET', 'POST'))
def delete():
    if request.method == 'POST':
        delete_transformer_data()
        insert_transformer_data(0,0,0,0,0)
        return redirect(url_for('plot'))

@app.route('/', methods = ('GET', 'POST'))
def login():
    if (request.method=='POST'):
        username = request.form['username']
        password = request.form['password']

        succeed = checklogin(username, password)
        if (succeed):
            session['username'] = username
            #global m_user
            #m_user = username
            flash('Welcome! Login Successful')
            return redirect(url_for('plot'))
        else:
            flash('Error: Invalid Username or Password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

#design the web_api
@app.route('/update/key=<api_key>/temp=<int:temperature>/vll=<int:voltage_ll>/vln=<int:voltage_ln>/vne=<int:voltage_ne>/current=<int:current>', methods=['GET'])
def update(api_key, temperature, voltage_ll, voltage_ln, voltage_ne, current):
    if (api_key == API):
        insert_transformer_data(temperature, voltage_ll, voltage_ln, voltage_ne, current)
        return Response(status=200)
    else:
        return Response(status=500)
    

@app.route('/insert/<int:b1>/<int:b2>/<int:b3>/<int:b4>', methods=['GET','POST'])
def insert_input(b1, b2, b3, b4):
    insert_transformer_input(b1, b2, b3, b4)
    return Response(status=200)  

@app.route('/get_transformer_input', methods = ['GET'])
def get_all_input():
    data = get_transformer_input('all')
    data = str(data)
    data = data.strip('[]()')
    return str(data)

@app.route('/get_transformer_input/<id>', methods = ['GET'])
def get_input(id):
    transformer_input = get_transformer_input(id)
    transformer_input = str(transformer_input)
    transformer_input = transformer_input.strip('[]()')
    return str(transformer_input)


#fetch data to be plotted
@app.route('/get_data', methods=['GET', 'POST'])
def get_trans_data():
    data = get_transformer_data()
    data = str(data)
    data = data.strip('[]()')
    return str(data)

#logout of session
@app.route('/logout', methods=['POST'])
def log_out():
    session.pop("username")
    return redirect(url_for('login'))


