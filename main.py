#Importar 
from fastapi import FastAPI
from config.db import engine, Base
from middlewares.error import Error
from routers.movie import movie_router
from routers.auth import auth_router

#Instancia
app = FastAPI()
app.title = 'Ejemplo FastApi'
app.version = '0.0.1'

app.add_middleware(Error)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

