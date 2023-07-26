from pydantic import BaseModel

class UserBase(BaseModel):
    id: str | None
    username: str
    email: str
    rol: str
    
class UserIn(UserBase):
    plain_password: str

class UserOut(UserBase):
    pass

class UserDB(UserBase):
    hashed_password: str