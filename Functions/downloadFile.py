import streamlit as st
import webbrowser
from Functions.uploadFileToS3 import upload_file_to_s3


# function that opens up the downloaded link
def download_file(name, path):
    st.write("Downloading.....")
    url = upload_file_to_s3(name, path, "noaa-goes18", "the-data-guys")
    webbrowser.open_new_tab(url)
    st.write("Done.")