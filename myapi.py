from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import hashlib
import os
import sqlite3
from Functions.extractFiles import extract_files
from Functions.uploadFileToS3 import upload_file_to_s3
from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen
from Functions.databaseAuth import register_user


from Functions.apiModel import UserSignupSchema, UserLoginSchema
from Functions.auth_bearer import JWTBearer
from Functions.auth_handler import signJWT
from Functions.databaseAuth import get_db

app = FastAPI()

security = HTTPBasic()

# @app.get("/protected")
# async def protected_route(credentials: HTTPBasicCredentials = Depends(security), db = Depends(get_db("auth_data.db"))):
#     # get stored password
#     cursor = db.cursor()
#     print(credentials.password)
#     res = cursor.execute("SELECT * FROM api_auth WHERE username=?", (credentials.username))
#     user = res.fetchone()
#     # hash user passowrd
#     hashed = hashlib.sha256(credentials.password.encode())
#     if not user or user["password"] != hashed.hexdigest():
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     global user_authenticated
#     return {"message": "This is a protected route"}


# (station, year, day, hour)
@app.get("/geos-get-by-path/{station}/{year}/{day}/{hour}",dependencies=[Depends(JWTBearer("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYiIsImV4cGlyZXMiOjE2NzcxNzY2NjAuNzAyNzMyfQ.bMey_TvCn4KIy2OLIs0E-IE2HSuW7VyeCbJomSp10Os"))])
async def geos_get_files_path(station,year,day,hour):
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    result = extract_files("noaa-goes18",path)
    
    return result

@app.get("/nexrad-get-by-path/{year}/{month}/{day}/{station}",dependencies=[Depends(JWTBearer())])
async def nexrad_get_files_path(year,month,day,station):
    path = "{}/{}/{}/{}/".format(year,month,day,station)
    result = extract_files("noaa-nexrad-level2",path)
    return result

@app.get("/geos-download-by-path/{station}/{year}/{day}/{hour}/{filename}",dependencies=[Depends(JWTBearer())])
async def geos_download_files_path(station,year,day,hour,filename):
    path = "{}/{}/{}/{}/".format(station, year, day, hour)
    url = upload_file_to_s3(filename, path, "noaa-goes18", "the-data-guys")
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/nexrad-download-by-path/{year}/{month}/{day}/{station}/{filename}",dependencies=[Depends(JWTBearer())])
async def geos_download_files_path(year,month,day,station,filename):
    path = "{}/{}/{}/{}/".format(year,month,day,station)
    url = upload_file_to_s3(filename, path, "noaa-nexrad-level2", "the-data-guys")
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/geos-download-by-name/{filename}",response_class=HTMLResponse,dependencies=[Depends(JWTBearer())])
async def geos_download_files_name(filename):
    url = geos_url_gen(filename) 
    return """<a href={}> Click Here to download file  </a>""".format(url)

@app.get("/nexrad-download-by-name/{filename}",response_class=HTMLResponse,dependencies=[Depends(JWTBearer())])
async def nexrad_download_files_name(filename):
    url = nexrad_url_gen(filename) 
    return """<a href={}> Click Here to download file  </a>""".format(url)

#-----------------
# @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSignupSchema = Body()):
    print(user)

    conn = get_db("auth_data.db")
    cursor = conn.cursor()
    res = cursor.execute("SELECT username FROM api_auth")
    db_user = res.fetchall()
    cursor.close()
    conn.close()
    if user.username in db_user:
        raise HTTPException(status_code=401, detail="already username exists! Try again!")
    register_user(user.name,user.username,user.password)
    return signJWT(user.username)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body()):
    conn = get_db("auth_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM api_auth WHERE username=?", (user.username))
    db_user = res.fetchone()
    cursor.close()
    conn.close()
    # hash user passowrd
    hashed = hashlib.sha256(user.password.encode())
    if not db_user or db_user["password"] != hashed.hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return signJWT(user.username)
   