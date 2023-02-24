from pydantic import BaseModel, Field, EmailStr



class UserSignupSchema(BaseModel):
    name: str = Field()
    username: str = Field()
    password: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "name": "Joe Doe",
                "username": "joe99",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field()
    password: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "username": "joe@xyz.com",
                "password": "any"
            }
        }