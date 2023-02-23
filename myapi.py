from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import hashlib
import os
import sqlite3
from Functions.extractFiles import extract_files
from Functions.uploadFileToS3 import upload_file_to_s3
from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen

app = FastAPI()

security = HTTPBasic()


# User database
def get_db():
    db_path = os.getcwd() + "/auth_data.db"
    conn = sqlite3.connect(db_path,check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/protected")
async def protected_route(credentials: HTTPBasicCredentials = Depends(security), db = Depends(get_db)):
    # get stored password
    cursor = db.cursor()
    print(credentials.password)
    res = cursor.execute("SELECT * FROM api_auth WHERE username=?", (credentials.username))
    user = res.fetchone()
    # hash user passowrd
    hashed = hashlib.sha256(credentials.password.encode())
    if not user or user["password"] != hashed.hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    global user_authenticated
    return {"message": "This is a protected route"}


# (station, year, day, hour)
@app.get("/geos-get-by-path/{station}/{year}/{day}/{hour}")
async def geos_get_files_path(station,year,day,hour):
    if not user_authenticated:
          raise HTTPException(status_code=401, detail="Log In Please")
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    result = extract_files("noaa-goes18",path)
    
    return result

@app.get("/nexrad-get-by-path/{year}/{month}/{day}/{station}")
async def nexrad_get_files_path(year,month,day,station):
    path = "{}/{}/{}/{}/".format(year,month,day,station)
    result = extract_files("noaa-nexrad-level2",path)
    return result

@app.get("/geos-download-by-path/{station}/{year}/{day}/{hour}/{filename}")
async def geos_download_files_path(station,year,day,hour,filename):
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    url = upload_file_to_s3(filename, path, "noaa-goes18", "the-data-guys")
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/nexrad-download-by-path/{year}/{month}/{day}/{station}/{filename}")
async def geos_download_files_path(year,month,day,station,filename):
    path = "{}/{}/{}/{}/".format(year,month,day,station)
    url = upload_file_to_s3(filename, path, "noaa-nexrad-level2", "the-data-guys")
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/geos-download-by-name/{filename}",response_class=HTMLResponse)
async def geos_download_files_name(filename):
    url = geos_url_gen(filename) 
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/nexrad-download-by-name/{filename}")
async def nexrad_download_files_name(filename):
    url = nexrad_url_gen(filename) 
    return """<a href={}> Click Here to download file  </a>""".format(url)
