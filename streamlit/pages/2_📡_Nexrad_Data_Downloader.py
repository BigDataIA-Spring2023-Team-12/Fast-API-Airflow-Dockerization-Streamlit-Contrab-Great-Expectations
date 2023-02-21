import streamlit as st
import pandas as pd
import boto3
import time
import sqlite3
import webbrowser
import datetime 
import s3fs
import os
import io

# function to transfer files between two AWS buckets and create a download link 
def upload_file_to_s3(file_name, prefix, source_bucket_name, target_bucket_name):
    """
    Uploads a file from one publicly accessible S3 bucket to another S3 bucket and returns the URL of the uploaded file.
    Parameters:
    file_name (str): The name of the file to be uploaded.
    prefix (str): The prefix of the file to be uploaded.
    source_bucket_name (str): The name of the source S3 bucket.
    target_bucket_name (str): The name of the target S3 bucket.
    Returns:
    str: The URL of the uploaded file.
    """
    # Create an S3 client and an S3 resource
    s3_client = boto3.client('s3')
    session = boto3.Session(aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"])
    s3_resource = session.resource('s3')

    # Get file from source bucket
    # Create a source object from the S3 resource
    source_object = s3_resource.Object(source_bucket_name, file_name)
    # Get the content of the file from the source object
    file_content = source_object.get()['Body'].read()

    # Upload file to target bucket
    # Create a target object from the S3 resource
    target_object = s3_resource.Object(target_bucket_name, file_name)
    # Upload the content of the file to the target object
    target_object.upload_fileobj(io.BytesIO(file_content))
    # Print a message indicating that the file has been uploaded
    print(f"File {file_name} with prefix {prefix} uploaded to S3 bucket {target_bucket_name}.")

    # Return link to uploaded file
    # Construct the URL of the uploaded file
    uploaded_file_url = f"https://{target_bucket_name}.s3.amazonaws.com/{file_name}"
    return uploaded_file_url
# function extract files from s3 bucket
def extract_files(bucket_name, prefix):
    s3 = boto3.resource('s3')
    result = []
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        result.append(obj.key)
    return result
# function used get file by file name
def link_gen(input):
    station = input[:4]
    year = input[4:8]
    month = input[8:10]
    day = input[10:12]

    fs = "https://noaa-nexrad-level2.s3.amazonaws.com/{}/{}/{}/{}/{}".format(year,month,day,station,input)
    return fs


# function that opens up the downloaded link
def download_file(name,path):
    st.write("Downloading.....")
    url = upload_file_to_s3(name,path,"noaa-nexrad-level2","the-data-guys")
    webbrowser.open_new_tab(url)
    st.write("Done.")
# this function displays input_boxes for search by filename method

def search_by_path():

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
        print("This Works")
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
        download_file(file,path)
        st.session_state['log_df'] = st.session_state['log_df'].append({'filename':file,'time':datetime.datetime.now()},ignore_index=True)
        
    st.dataframe(st.session_state['log_df'])   
# this function displays input_boxes for search by file path method      
def search_by_filename():
    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    link = " "
    if st.button('Get Link!',key='getLink'):
        link = link_gen(filename_input)
    st.write("Link: {}".format(link))

connection = sqlite3.connect("../streamlit/meta_data.db")
cursor = connection.cursor()

st.write("# NexRad Data Downloader 📡")
search_method = st.selectbox(
        "Select Search Method",
        ["Search by Filename","Search by Path"]
        )

if search_method == "Search by Path":
    search_by_path()
if search_method == "Search by Filename":
    search_by_filename()



    