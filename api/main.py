from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register, user
app = FastAPI()
app.include_router(login.router)
app.include_router(user.router)
app.include_router(register.router)

origins = [
    'http://127.0.0.1:5500',
    'http://127.0.0.1',
]

app.add_middleware(CORSMiddleware, 
                   allow_origins = origins, 
                   allow_credentials = True, 
                   allow_methods = ["*"], 
                   allow_headers = ["*"])

@app.get('/')
async def root():
    return 'Conectando a la base de datos'

