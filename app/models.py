import sqlite3 as sql
from datetime import datetime

def insert_transformer_data(temperature, voltage_l_l, voltage_l_n, voltage_n_e, current):
    con = sql.connect("gp.db")
    cur = con.cursor()
    #add datetime to the query
    cur.execute("INSERT INTO transformer_data(temperature, voltage_l_l, voltage_l_n, voltage_n_e, current) VALUES (?,?,?,?,?)", (temperature, voltage_l_l, voltage_l_n, voltage_n_e, current))# datetime.now()
    con.commit()
    con.close()

def insert_transformer_input(c1, c2, c3, c4):
    c1 = f"{c1}"
    c2 = f"{c2}"
    c3 = f"{c3}"
    c4 = f"{c4}"
    con = sql.connect("gp.db")
    cur = con.cursor()
    query = f"UPDATE ranges SET c1 = {c1}, c2 = {c2}, c3 = {c3}, c4 = {c4} WHERE id = 1"
    cur.execute(query)
    con.commit()
    con.close()

def get_transformer_input(id):
    id = f"{id}"
    con = sql.connect("gp.db")
    cur = con.cursor()

    if id == 'all':
        query = f"SELECT c1, c2, c3, c4 FROM ranges WHERE id = 1"
    else:
        query = f"SELECT {id} FROM ranges WHERE id = 1"
    cur.execute(query)
    control_input = cur.fetchall()
    con.commit()
    con.close()
    return control_input

def checklogin(username, password):
    con = sql.connect("gp.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()

    if username == users[0][0] and password == users[0][1]:
        success = True
    else:
        success = False
    con.commit()
    con.close()
    return success

def get_transformer_data():
    con = sql.connect("gp.db")
    cur = con.cursor()
    #get the latest data
    cur.execute("SELECT * FROM transformer_data ORDER BY id DESC LIMIT 40")
    t_data = cur.fetchall()
    con.commit()
    con.close()
    return t_data

def delete_transformer_data():
    con = sql.connect("gp.db")
    cur = con.cursor()
    cur.execute("DELETE FROM transformer_data")
    con.commit()
    con.close()