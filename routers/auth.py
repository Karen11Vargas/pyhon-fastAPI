from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from schemas.user import User

auth_router = APIRouter()

@auth_router.post('/login', tags=['Auth'])
def login(user:User):
    if user.email == "kali@gmail.com" and user.password =="123":
        token: str = create_token(user.dict())
        return JSONResponse(content=token)
