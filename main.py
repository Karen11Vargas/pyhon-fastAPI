#Importar 
from fastapi import FastAPI, Body

#Instancia
app = FastAPI()
app.title = 'Ejemplo FastApi'
app.version = '0.0.1'

movies = [ { "id" : 1,"name" : "Last OF US", "category" : "History", "year" : 2024},{ "id" : 2,"name" : "Deadpool", "category" : "History", "year" : 2025}]

@app.get('/', tags=['Home'])
def greeting():
    return 'Hello Word'

@app.get('/movies', tags=['Movies'])
def all():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def movies_filter(id:int):
    return list(filter(lambda x: x['id'] == id, movies))

#Parametros Query, se pasa el parametro en la funcion y no en la etiqueta
@app.get('/movies/', tags=['Movies'])
def movies_query(year:int,  category:str):
    result = [movie for movie in movies if movie['year'] == year and movie['category'] == str.capitalize(category)  ]
    return result

#Parametros Query, se pasa el parametro en la funcion y no en la etiqueta
@app.post('/movies', tags=['Movies'])
def movies_create(id: int = Body(), name:str  = Body(), year:int  = Body(),  category:str  = Body()):
    for m in movies:
        if m['id'] == id:
            return "Id ya existe"
    
    movies.append({
        "id": id,
        "name": name,
        "category": category,
        "year": year
    })

    return movies

#Put
@app.put('/movies/{id}', tags=['Movies'])
def movies_update(id: int, name:str  = Body(), year:int  = Body()):
    for m in movies:
        if m['id'] == id:
            m.remove({
                "name": name,
                "year" :year
            })
            return movies

        else:
            return "Id No existe"


#Delete
@app.delete('/movies/{id}', tags=['Movies'])
def movies_delete(id: int):
    for m in movies:
        if m['id'] == id:
            movies.remove(m)
            return movies
        else:
            return "Id No existe"
    return movies