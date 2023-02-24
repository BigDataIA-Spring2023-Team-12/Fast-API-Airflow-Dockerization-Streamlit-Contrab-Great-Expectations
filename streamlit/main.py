import streamlit as st
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import sqlite3
import plotly.graph_objects as go
import pandas as pd
from streamlit_option_menu import option_menu
from Functions.searchByFilename import geos_search_by_filename
from Functions.searchByFilename import nexrad_search_by_filename
from Functions.searchByPath import geos_search_by_path
from Functions.searchByPath import nexrad_search_by_path
from Functions.databaseAuth import get_user_auth_table
from Functions.databaseAuth import register_user



st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
# --- CONNECT TO PASSWORD DATABAE ---
#--- REGISTER USER ---

# --- USER AUTHENTICATION ---
auth_df = get_user_auth_table() 
names = auth_df['name'].tolist()
usernames = auth_df['username'].tolist()
hashed_passwords = auth_df['password'].tolist()
# usernames = ['a']
# hashed_passwords = ['$2b$12$ygMdN2YIYMgcpixCfIQTI.6WDtnEB7Qy8kx7WoGjMPkh49jRIdxd2']
# names = ['a']
cookie_expiry_days = 3
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "file_downloader", # name of the cookie stored in a the users browser 
    "abcdef", # random key to hash cookie signature
    cookie_expiry_days
    )

name,authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # --- OPTION MENU ----
    selected = option_menu(
    menu_title = None,
    options = ["Home","GEOS","NexRad","Locations"],
    icons = ["house-door","rocket","airplane","geo-fill"],
    default_index = 0,
    orientation = "horizontal"
    )
    if selected == "Home":
        st.write("# Welcome! 👋")
        st.markdown(
            """
            # Assignment 1
            ## Team 14
            - Parva Shah 
            - Dev Shah
            - Harsh Shah

            This streamlit app has 3 pages:
            - 1_🛰_Geos_Data_Downloader:

                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 2_📡_Nexrad_Data_Downloader
            
                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 3_📍_NexRad_Locations
                This plots the Nexrad locations on the US map

        """
        )

    if selected == "GEOS":
        connection = sqlite3.connect("../streamlit/meta_data.db")
        cursor = connection.cursor()

        st.write("# GEOS Satellite Data Downloader 🛰")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            geos_search_by_path(cursor)
        if search_method == "Search by Filename":
            geos_search_by_filename()

    if selected == "NexRad":
        connection = sqlite3.connect("../streamlit/meta_data.db")
        cursor = connection.cursor()

        st.write("# NexRad Data Downloader 📡")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            nexrad_search_by_path(cursor)
        if search_method == "Search by Filename":
            nexrad_search_by_filename()

    if selected == "NexRad Locations":
        st.write("# Nexrad Locations in USA 📍")
      #filename issue
        df = pd.read_csv('../../ass-1/streamlit/nexrad_loc.csv')
        df['text'] = 'City: ' + df['City'] + ', ' + 'State: ' + df["State"] + ', ' + 'Identifier: ' + df[
            'ICAO Location Identifier'].astype(str)

        fig = go.Figure(data=go.Scattergeo(
            lon=df['Long'],
            lat=df['Lat'],
            text=df['text'],
            mode='markers',
        ))

        fig.update_layout(
            title='NexRad Locations',
            geo_scope='usa',
            geo=dict(bgcolor='rgba(0,0,0,0)',
                    lakecolor='#4E5D6C',
                    landcolor='rgba(51,17,0,0.2)',
                    subunitcolor='grey'),

        )
        st.plotly_chart(fig, use_container_width=True)


    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")

    
st.sidebar.write('## Sign up')
name = st.sidebar.text_input('Name')   
username = st.sidebar.text_input('Username')
password = st.sidebar.text_input('Password', type='password')
confirm_password = st.sidebar.text_input('Confirm Password', type='password')
if password == confirm_password:
    st.sidebar.write("Password Match!")
    if st.sidebar.button('Sign up'):
        register = register_user(name,username,password)
if password != confirm_password:
    st.sidebar.write("Passwords don't match, Try Again!")  


   









