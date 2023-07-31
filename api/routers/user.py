from fastapi import APIRouter, HTTPException, status, Depends
from db.client import db
from db.models.user import UserOut, UserIn, UserDB
from passlib.context import CryptContext
from bson import ObjectId
from db.models.user import UserIn, UserOut, UserDB
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix='/user', 
                   tags=['User'],
                   responses={
                       status.HTTP_200_OK: {'message': 'Información correcta'},
                       status.HTTP_400_BAD_REQUEST: {'message': 'Información incorrecta'}
                   })
pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "3bf9cac2aee8eaeaafb3cfd8bdaedd7d9a1e68bf8c0321dd9d3b8d476c548dc3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 10


def search_user(key: str, value: str | ObjectId):
    return db.users.find_one({key: value})


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Token inválido', 
            headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('sub')
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = search_user('_id', ObjectId(id))
    if user is None:
        raise credentials_exception
    return UserOut(**user)


@router.get('/me', 
            response_model=UserOut, 
            status_code=status.HTTP_200_OK, 
            responses={
                status.HTTP_200_OK: {'description': 'Respuesta afirmativa'},
                status.HTTP_400_BAD_REQUEST: {'description': 'No encontrado'}
            },
            name='Obtener usuario por token',
            description='En la petición HTTP se debe enviar el access token en el header, con Authorization: bearer + token')
async def get_user_by_token(current_user: UserIn = Depends(get_current_user)):
    return current_user


