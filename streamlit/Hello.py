import streamlit as st
import pandas as pd
import boto3
import time
import sqlite3
import json

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome! 👋")

st.sidebar.success("Select a demo above.")

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








