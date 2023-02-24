import sqlite3
import pandas as pd
import streamlit as st
import hashlib
import os
import streamlit_authenticator as stauth

# create table in the sqlite databae
# conn = sqlite3.connect("../auth_data.db")
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS api_auth (username TEXT , password TEXT,PRIMARY KEY (username))")   
 

def get_db(db):
    db_path = os.getcwd() + "/{}".format(db)
    conn = sqlite3.connect(db_path,check_same_thread=False)
    return conn

def get_user_auth_table():
    conn = get_db("auth_data.db")
    cursor = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM user_auth", conn)
    return df

# Sign-up page
def register_user(name,username,password):
    conn = get_db("auth_data.db")
    cursor = conn.cursor()
    hashed_password = stauth.Hasher([password]).generate()
    # used a different hasher for api authentication using hashlib
    result = hashlib.sha256(password.encode())
    # Execute the INSERT query to add the row to the table
    query = "INSERT INTO user_auth (name,username, password) VALUES (?, ?, ?)"
    cursor.execute(query, (name,username, hashed_password[0]))

    query = "INSERT INTO api_auth (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, result.hexdigest()))

    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # cursor.execute("INSERT INTO auth_data VALUES ({},{})".format(username,hashed_password))   
    return st.success('You have successfully signed up! Log in please!')

