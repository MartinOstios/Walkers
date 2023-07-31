from fastapi import APIRouter, HTTPException, status
from db.models.user import UserIn, UserOut, UserDB
from db.schemas.user import password_hash, search_user
from db.client import db
router = APIRouter(tags=['Register'])

@router.post('/register',
            response_model=UserOut,
            status_code=status.HTTP_201_CREATED,
            name='Registro',
            response_description='Usuario creado satisfactoriamente')
async def register(user: UserIn):
    user_db = search_user('username', user.username)
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already in DB')
    id = db.users.insert_one({'username': user.username,
                              'email': user.email,
                              'rol': user.rol,
                              'password': password_hash(user.plain_password)}).inserted_id
    user = UserOut(**user.dict())
    user.id = str(id)
    return user


