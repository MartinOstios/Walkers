from fastapi import FastAPI
from routers import login, user
app = FastAPI()
app.include_router(login.router)
app.include_router(user.router)

@app.get('/')
async def root():
    return 'Conectando a la base de datos'

