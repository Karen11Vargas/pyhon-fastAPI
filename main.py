#Importar 
from fastapi import FastAPI

#Instancia
app = FastAPI()
app.title = 'Ejemplo FastApi'
app.version = '0.0.1'

movies = [ { "id" : 1,"name" : "Last OF US", "category" : "History","year" : 2024}]

@app.get('/', tags=['Home'])
def greeting():
    return 'Hello Word'

@app.get('/movies', tags=['Movies'])
def greeting():
    return movies