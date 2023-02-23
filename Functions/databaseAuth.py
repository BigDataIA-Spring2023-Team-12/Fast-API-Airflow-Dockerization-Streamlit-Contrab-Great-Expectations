import sqlite3
import pandas as pd
import streamlit as st
import hashlib
import streamlit_authenticator as stauth

# # create table in the sqlite databae
# conn = sqlite3.connect("../streamlit/auth_data.db")
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS user_auth ( name TEXT, username TEXT , password TEXT)")   
 



def get_user_auth_table():
    conn = sqlite3.connect("../streamlit/auth_data.db")
    cursor = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM user_auth", conn)
    return df

# Sign-up page
def register_user(name,username,password):
    conn = sqlite3.connect("../streamlit/auth_data.db")
    cursor = conn.cursor()
    hashed_password = stauth.Hasher([password]).generate()
    # Execute the INSERT query to add the row to the table
    query = "INSERT INTO user_auth (name,username, password) VALUES (?, ?, ?)"
    cursor.execute(query, (name,username, hashed_password[0]))
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # cursor.execute("INSERT INTO auth_data VALUES ({},{})".format(username,hashed_password))   
    return st.success('You have successfully signed up! Log in please!')

