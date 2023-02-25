import unittest
from fastapi.testclient import TestClient
from myapi import app
from myapi import JWTBearer


# def mock_dependency():
#     return "mocked dependency"

# app.dependency_overrides[JWTBearer] = mock_dependency

class TestApp(unittest.TestCase):
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYiIsImV4cGlyZXMiOjE2NzcyNzk0NzUuODQ5OTc5OX0.IV0EUP461EvhHo8LApbRsybEMkJ6i4rkxxGITD1bhuQ"
    def setUp(self):
        self.client = TestClient(app)
    
    def test_create_user(self):
        response = self.client.post("/user/signup", json={"name":"parva shah","username": "dev4", "password":"parva"})
        print(response)
        self.assertEqual(response.status_code, 200)
        
    
    def test_user_login(self):
        response = self.client.post("/user/login", json={"username": "b", "password":"b"})
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_geos_get_files_path(self):
        response = self.client.get("/geos-get-by-path/ABI-L1b-RadC/2022/209/02", headers = {"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYiIsImV4cGlyZXMiOjE2NzcyODA4ODUuNzQ0MjgzfQ.PWYzF571n2h69X6n9seE5bagyJJ5PIyxB0kVvdC2eL0"})
        self.assertEqual(response.status_code, 200)
    
    def test_nexrad_get_files_path(self):
        response = self.client.get("/nexrad-get-by-path/2022/01/01/KAKQ")
        self.assertEqual(response.status_code, 200)
    
    def test_geos_download_files_path(self):
        response = self.client.get("/geos-download-by-path/ABI-L1b-RadC/2022/209/02/OR_ABI-L1b-RadC-M6C01_G18_s20222090201140_e20222090203513_c20222090203554.nc")
        self.assertEqual(response.status_code, 200)
    
    def test_nexrad_download_files_path(self):
        response = self.client.get("/nexrad-download-by-path/2022/01/01/KAKQ/KAKQ20220101_000149_V06")
        print(response)
        self.assertEqual(response.status_code, 200)
    
    def test_geos_download_files_name(self):
        response = self.client.get("/geos-download-by-name/OR_ABI-L1b-RadC-M6C01_G18_s20222090201140_e20222090203513_c20222090203554.nc")
        print(response)
        self.assertEqual(response.status_code, 200)

    
    def test_nexrad_download_files_name(self):
        response = self.client.get("/nexrad-download-by-name/KAKQ20220101_000149_V06")
        print(response)
        self.assertEqual(response.status_code, 200)
        
    
        

    