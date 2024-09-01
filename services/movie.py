from models.movie import Movie as MovieModel
from config.db import Session

class MovieService():
    db = Session()
    # def __init__(self) -> None:
    #     self.db = Session

    def all_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def filter_movies(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def query_movies(self, year, category):
        result = self.db.query(MovieModel).filter(MovieModel.year == year, MovieModel.category == category).all()
        return result
    
    def new_movies(self, movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return "Ingresado Correctamente"

    def update_movies(self, id, movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result :
            return ("El ID NO existe", 400)
        result.name = movie.name
        result.year = movie.year
        self.db.commit()
        return ("Ingresado Correctamente", 201)

    def delete_movies(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result :
            return  ("El ID NO existe", 400)
        #Elimina el objeto pero no ejecuta la eliminacion en la bd
        self.db.delete(result)
        #Ejecuta las acciones que se indiquen
        self.db.commit()
        return ("Eliminado Correctamente", 201)
