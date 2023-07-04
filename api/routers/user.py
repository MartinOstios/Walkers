from fastapi import APIRouter, HTTPException, status
from db.client import db
from db.models.user import UserOut, UserIn, UserDB
from db.schemas.user import user_schema
from passlib.context import CryptContext
from bson import ObjectId

router = APIRouter(prefix='/user')
pwd_context = CryptContext(schemes=['bcrypt'])

# Password hash
def password_hash(password: str):
    return pwd_context.hash(password)


def search_user(key: str, value: str | ObjectId):
    return db.users.find_one({key: value})

@router.post('/')
async def create_user(user: UserIn):
    # Revisar que no exista un usuario con el mismo correo
    user_db = search_user('email', user.email)
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already in DB')
    id = db.users.insert_one({'username': user.username,
                              'email': user.email,
                              'password': password_hash(user.plain_password)}).inserted_id
    user = UserOut(**user.dict())
    user.id = str(id)
    return user

@router.get('/{id}')
async def get_user(id: str):
    user_db = search_user('_id', ObjectId(id))
    user_db = {'id': str(user_db['_id']), 'username': user_db['username'], 'email': user_db['email'], 'hashed_password': user_db['password']}
    return UserDB(**user_db)