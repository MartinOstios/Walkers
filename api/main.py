from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return 'Conectando a la base de datos'

