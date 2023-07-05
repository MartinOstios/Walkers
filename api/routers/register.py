from fastapi import APIRouter, HTTPException, status
from db.models.user import UserIn, UserOut, UserDB
from db.client import db
from bson import ObjectId
from passlib.context import CryptContext
router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'])


def password_hash(password: str):
    return pwd_context.hash(password)

def search_user(key: str, value: str | ObjectId):
    return db.users.find_one({key: value})

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    user_db = search_user('email', user.email)
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already in DB')
    id = db.users.insert_one({'username': user.username,
                              'email': user.email,
                              'password': password_hash(user.plain_password)}).inserted_id
    user = UserOut(**user.dict())
    user.id = str(id)
    return user


