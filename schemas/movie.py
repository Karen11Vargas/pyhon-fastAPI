from pydantic import BaseModel, Field
from typing import Optional

class Model(BaseModel):
    #nombre  tipo   si es opcional y valor por defecto
         
    name:     str = Field(default = "Mi peli", min_length = 5, max_length= 20)
    category: Optional[str] = None
    year:     int

    model_config  ={
        "json_schema_extra":{
            "examples":[
                {
                    "name":"Mi pelicula",
                    "category": "Terror",
                    "year": 2023
                }
            ]
        }
    }