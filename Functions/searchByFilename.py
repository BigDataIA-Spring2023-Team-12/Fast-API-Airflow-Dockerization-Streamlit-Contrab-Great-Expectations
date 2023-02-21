import streamlit as st
from urlGen import url_gen


# this function displays input_boxes for search by filename method
def search_by_filename():
    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    link = " "
    if st.button('Get Link!', key='getLink'):
        link = url_gen(filename_input)
    st.write("Link: {}".format(link))
