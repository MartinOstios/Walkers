from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas.user import search_user, verify_password
from jose import jwt
from datetime import datetime, timedelta
router = APIRouter(tags=['Login'])

SECRET_KEY = "3bf9cac2aee8eaeaafb3cfd8bdaedd7d9a1e68bf8c0321dd9d3b8d476c548dc3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 10


def authenticate_user(username: str, password: str):
    user = search_user('username', username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post('/login', response_model=dict, status_code=status.HTTP_200_OK, description='Valida la información del usuario y devuelve un access token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(data={'sub': user.id}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt