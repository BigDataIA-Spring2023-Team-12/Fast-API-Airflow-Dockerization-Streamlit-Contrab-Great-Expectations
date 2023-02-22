import streamlit as st
from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen


# this function displays input_boxes for search by filename method
def geos_search_by_filename():
    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    link = " "
    if st.button('Get Link!', key='getLink'):
        link = geos_url_gen(filename_input)
    st.write("Link: {}".format(link))

# this function displays input_boxes for search by file path method      
def nexrad_search_by_filename():
    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    link = " "
    if st.button('Get Link!',key='getLink'):
        link = nexrad_url_gen(filename_input)
    st.write("Link: {}".format(link))

