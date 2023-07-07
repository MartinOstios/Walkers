from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.models.user import UserIn, UserOut, UserDB
from db.schemas.user import search_user, verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
router = APIRouter()

SECRET_KEY = "3bf9cac2aee8eaeaafb3cfd8bdaedd7d9a1e68bf8c0321dd9d3b8d476c548dc3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 1


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(username: str, password: str):
    user = search_user('username', username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Token inválido', 
            headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'payload {payload}')
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = search_user('username', username)
    if user is None:
        raise credentials_exception
    return UserOut(**user.dict())


@router.get('/users/me')
async def get_user_by_token(current_user: UserIn = Depends(get_current_user)):
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt