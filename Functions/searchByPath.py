import streamlit as st
import pandas as pd
import datetime
from Functions.extractFiles import extract_files
from Functions.downloadFile import download_file


# this function displays input_boxes for search by file path method
def geos_search_by_path(cursor):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        station_val = cursor.execute("SELECT DISTINCT station FROM geos")
        station = st.selectbox(
            'Which Station ?',
            [i[0] for i in station_val]
        )

    with col2:
        year_val = cursor.execute("SELECT DISTINCT year FROM geos WHERE station = '{}' ".format(station))
        year = st.selectbox(
            'What Year ?',
            [i[0] for i in year_val],
        )
    with col3:
        day_val = cursor.execute(
            "SELECT DISTINCT day FROM geos WHERE station = '{}' AND year = '{}'".format(station, year))
        day = st.selectbox(
            'What Day ?',
            [i[0] for i in day_val],
        )
    with col4:
        hour_val = cursor.execute(
            "SELECT DISTINCT hour FROM geos WHERE station = '{}' AND year = '{}' AND day = '{}'".format(station, year,
                                                                                                        day))
        hour = st.selectbox(
            'What Hour ?',
            [i[0] for i in hour_val],
        )
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    df_list = []

    if not st.session_state.get('button'):
        st.session_state['button'] = True

    if st.session_state['button']:
        directories = extract_files("noaa-goes18", path)
        df = pd.DataFrame({"name": directories})
        df_list = [i for i in df["name"]]

    file = st.selectbox(
        'Select file to download',
        df_list,
        key="filename"
    )

    st.write("You selected:", file)
    download_btn = st.button("Download File")

    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename', 'time'])

    if download_btn:
        download_file(file, path,"noaa-goes18")
        st.session_state['log_df'] = st.session_state['log_df'].append(
            {'filename': file, 'time': datetime.datetime.now()}, ignore_index=True)

    st.dataframe(st.session_state['log_df'])


def nexrad_search_by_path(cursor):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        year_val = cursor.execute("SELECT DISTINCT year FROM nexrad")
        year = st.selectbox(
            'Which Year ?',
            [i[0] for i in year_val]
            )

    with col2:
        month_val = cursor.execute("SELECT DISTINCT month FROM nexrad WHERE year = '{}' ".format(year))
        month = st.selectbox(
            'What Month ?',
            [i[0] for i in month_val]
        )
    with col3:
        day_val = cursor.execute("SELECT DISTINCT day FROM nexrad WHERE year = '{}' AND month = '{}'".format(year,month))
        day = st.selectbox(
            'What Day ?',
            [i[0] for i in day_val]
        )
    with col4:
        station_val = cursor.execute("SELECT DISTINCT station FROM nexrad WHERE year = '{}' AND month = '{}' AND day = '{}'".format(year,month,day))
        station = st.selectbox(
            'Which Station ?',
            [i[0] for i in station_val]
        )
    path = "{}/{}/{}/{}/".format(year,month,day,station)

    if st.session_state.get('button')!=True:
        st.session_state['button'] = True

    if st.session_state['button']==True:
        directories = extract_files("noaa-nexrad-level2", path)
        df = pd.DataFrame({"name":directories})
        df_list = [i for i in df["name"]]
    
    file = st.selectbox(
            'Select file to download',
            df_list,
            key = "filename"
        )
    st.write("You selected:", file)
    download_btn = st.button("Download File")
    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename','time'])

    if download_btn:
        download_file(file,path,"noaa-nexrad-level2")
        st.session_state['log_df'] = st.session_state['log_df'].append({'filename':file,'time':datetime.datetime.now()},ignore_index=True)
        
    st.dataframe(st.session_state['log_df'])


