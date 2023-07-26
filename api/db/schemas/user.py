from passlib.context import CryptContext
from db.client import db
from bson import ObjectId
from db.models.user import UserDB
pwd_context = CryptContext(schemes=['bcrypt'])


def user_schema(user) -> UserDB | None:
    if user:
        return UserDB(id=str(user['_id']), username=user['username'], email=user['email'], rol=user['rol'], hashed_password= user['password'])
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def password_hash(password):
    return pwd_context.hash(password)
    
def search_user(key: str, value: str | ObjectId) -> UserDB | None:
    return user_schema(db.users.find_one({key: value}))