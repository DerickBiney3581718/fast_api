from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserResponseSchema(BaseModel):
    email:str