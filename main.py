#Importar 
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Optional, List
#Instancia
app = FastAPI()
app.title = 'Ejemplo FastApi'
app.version = '0.0.1'


#Esquema
class Model(BaseModel):
    #nombre  tipo   si es opcional y valor por defecto
    id:       int       
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


movies = [ { "id" : 1,"name" : "Last OF US", "category" : "History", "year" : 2024},{ "id" : 2,"name" : "Deadpool", "category" : "History", "year" : 2025}]

@app.get('/', tags=['Home'])
def greeting():
    return 'Hello Word'

@app.get('/movies', tags=['Movies'], response_model=List[Model])
def all()-> List[Model]:
    return JSONResponse(content=movies)

#Validación Path
@app.get('/movies/{id}', tags=['Movies'],  response_model=Model)
def movies_filter(id:int= Path(ge=1, le=100)) -> Model:
    data = list(filter(lambda x: x['id'] == id, movies))
    return JSONResponse(content=data)

#Parametros Query, se pasa el parametro en la funcion y no en la etiqueta
@app.get('/movies/', tags=['Movies'],  response_model=List[Model])
def movies_query(year:int = Query(ge=2022, le=2024),  category:str = Query(max_length=5))->List[Model]:
    result = [movie for movie in movies if movie['year'] == year and movie['category'] == str.capitalize(category)  ]
    return JSONResponse(content=result)

#Crear
@app.post('/movies', tags=['Movies'],  response_model=dict)
def movies_create(movie: Model)-> dict:
    for m in movies:
        if m['id'] == movie.id:
            return JSONResponse(content={"status_code":400,"message":"El ID ya existe"}, status_code=400)
    
    movies.append(movie)

    return JSONResponse(content={"message":"Ingresado Correctamente"},status_code=200 )

#Put
@app.put('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_update(id: int, movie: Model)->dict:
    for m in movies:
        if m['id'] == id:
            m.update({
                "name": movie.name,
                "year": movie.year,
                "id" : id
            })
        return JSONResponse(content={"status_code":201,"message":"Actualizado"}, status_code=201)
        
    return JSONResponse(content={"status_code":400,"message":"El ID NO existe"}, status_code=400)


#Delete
@app.delete('/movies/{id}', tags=['Movies'],   response_model=dict)
def movies_delete(id: int) ->dict:
    for m in movies:
        if m['id'] == id:
            movies.remove(m)
            return movies
        else:
            return JSONResponse(content={"status_code":400,"message":"El ID NO existe"}, status_code=400)

    return JSONResponse(content={"status_code":200,"message":"Eliminado"}, status_code=200)
