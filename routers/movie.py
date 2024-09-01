from fastapi import  Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_validation import JWTBearer

#Importar db
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from schemas.movie import Model
from services.movie import MovieService

movie_router = APIRouter()


@movie_router.get('/movies', tags=['Movies'], response_model=List[Model], dependencies=[Depends(JWTBearer())])
def all()-> List[Model]:
    
    data= MovieService().all_movies()

    return JSONResponse(status_code=200, content=jsonable_encoder(data))

#Validación Path
@movie_router.get('/movies/{id}', tags=['Movies'],  response_model=Model)
def movies_filter(id:int= Path(ge=1, le=100)) -> Model:

    
    data = MovieService().filter_movies(id)
    if not data:
        return JSONResponse(content="No encontrado")
    return JSONResponse(content=jsonable_encoder(data))

#Parametros Query, se pasa el parametro en la funcion y no en la etiqueta
@movie_router.get('/movies/', tags=['Movies'],  response_model=List[Model])
def movies_query(year:int = Query(ge=2022, le=2024),  category:str = Query(max_length=20))->List[Model]:
    
    data = MovieService().query_movies(year,category)
    if not data:
        return JSONResponse(content="No encontrado")
    return JSONResponse(content=jsonable_encoder(data))

#Crear
@movie_router.post('/movies', tags=['Movies'],  response_model=dict)
def movies_create(movie: Model)-> dict:
    
    response = MovieService().new_movies(movie)
    
    return JSONResponse(content={"message":response},status_code=200 )

#Put
@movie_router.put('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_update(id: int, movie: Model)->dict:

    
    result = MovieService().update_movies(id,movie)
    
    return JSONResponse(content={"status_code":result[1],"message":result[0]}, status_code=result[1])
        

#Delete
@movie_router.delete('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_delete(id: int) ->dict:
    
    result = MovieService().delete_movies(id) 
    return JSONResponse(content={"status_code":result[1],"message":result[0]}, status_code=result[1])
