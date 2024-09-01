#Importar 
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

#Importar db
from config.db import Session, engine, Base
from models.movie import Movie
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
#Instancia
app = FastAPI()
app.title = 'Ejemplo FastApi'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

#Esquemas
class Model(BaseModel):
    #nombre  tipo   si es opcional y valor por defecto
         
    name:     str = Field(default = "Mi peli", min_length = 5, max_length= 20)
    category: Optional[str] = None
    year:     int

    model_config  ={
        "json_schema_extra":{
            "examples":[
                {
                    "id":1,
                    "name":"Mi pelicula super hipermega interesante",
                    "category": "Terror",
                    "year": 2023
                }
            ]
        }
    }

class User(BaseModel):
    email:str
    password:str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "kali@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales Invalidas")

# movies = [ { "id" : 1,"name" : "Last OF US", "category" : "History", "year" : 2024},{ "id" : 2,"name" : "Deadpool", "category" : "History", "year" : 2025}]

@app.get('/', tags=['Home'])
def greeting():
    return 'Hello Word'

@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == "kali@gmail.com" and user.password =="123":
        token: str = create_token(user.dict())
        return JSONResponse(content=token)

@app.get('/movies', tags=['Movies'], response_model=List[Model], dependencies=[Depends(JWTBearer())])
def all()-> List[Model]:
    db = Session()
    data= db.query(MovieModel).all()

    return JSONResponse(status_code=200, content=jsonable_encoder(data))

#Validación Path
@app.get('/movies/{id}', tags=['Movies'],  response_model=Model)
def movies_filter(id:int= Path(ge=1, le=100)) -> Model:

    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
        return JSONResponse(content="No encontrado")
    return JSONResponse(content=jsonable_encoder(data))

#Parametros Query, se pasa el parametro en la funcion y no en la etiqueta
@app.get('/movies/', tags=['Movies'],  response_model=List[Model])
def movies_query(year:int = Query(ge=2022, le=2024),  category:str = Query(max_length=20))->List[Model]:
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.year == year, MovieModel.category == category).all()
    if not data:
        return JSONResponse(content="No encontrado")
    return JSONResponse(content=jsonable_encoder(data))

#Crear
@app.post('/movies', tags=['Movies'],  response_model=dict)
def movies_create(movie: Model)-> dict:
    db = Session()

    #se pasa la info que se va a oasar
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()

    return JSONResponse(content={"message":"Ingresado Correctamente"},status_code=200 )

#Put
@app.put('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_update(id: int, movie: Model)->dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result :
        return JSONResponse(content={"status_code":400,"message":"El ID NO existe"}, status_code=400)
    result.name = movie.name
    result.year = movie.year
    db.commit()
    
    return JSONResponse(content={"status_code":201,"message":"Actualizado"}, status_code=201)
        

#Delete
@app.delete('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_delete(id: int) ->dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result :
        return JSONResponse(content={"status_code":400,"message":"El ID NO existe"}, status_code=400)
    #Elimina el objeto pero no ejecuta la eliminacion en la bd
    db.delete(result)
    #Ejecuta las acciones que se indiquen
    db.commit()
    return JSONResponse(content={"status_code":200,"message":"Eliminado"}, status_code=200)
