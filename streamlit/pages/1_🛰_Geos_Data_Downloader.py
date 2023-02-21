import streamlit as st
import sqlite3
from Functions.searchByFilename import search_by_filename
from Functions.searchByPath import search_by_path


connection = sqlite3.connect("../streamlit/meta_data.db")
cursor = connection.cursor()

st.write("# GEOS Satellite Data Downloader 🛰")
search_method = st.selectbox(
    "Select Search Method",
    ["Search by Filename", "Search by Path"]
)

if search_method == "Search by Path":
    search_by_path(cursor)
if search_method == "Search by Filename":
    search_by_filename()
