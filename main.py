from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from arango import ArangoClient
from user.database import db
import os
from user import schema as schemas
from user.user import *
from uuid import UUID, uuid4

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def read_root():
    return {"message": "Hello asd"}


@app.post("/create_new_user",
                status_code=200,
                name="Create new user",
                tags=["User"])
async def create_new_user(data: schemas.CreateUser = Body(...)):
    try:
        user = User(user_data=data)
        return user.create_token()

    except Exception as e:
        print(e)
        raise ValueError

@app.post("/login",
                status_code=200,
                name="Login",
                tags=["User"])
async def login(data: schemas.Login = Body(...)):
    try:
        user = User.by_email(str(data.email))
        if user.check_password(str(data.password)):    
            return user.create_token()
        
        else:
            raise ValueError

    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid password")

@app.post("/check_token",
                status_code=200,
                name="Check token",
                tags=["User"])
async def check_token(token: str):
    try:
        return User.check_token(token)

    except Exception as e:
        print(e)

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    try:
        user = User.by_id(str(user_id))
        document = json.loads(schemas.UserPrivate.parse_obj(user.data).json())
        del document["password"]
        return schemas.UserPublic.parse_obj(document)

    except Exception as e:
        print(e)


@app.patch("/change_user",
                status_code=200,
                name="Change user",
                tags=["User"])
async def change_user(data: schemas.PatchUser = Body(...)):
    try:
        user = User(id=data.id)
        user.update(json.loads(data.json()))
        return user.create_token()

    except Exception as e:
        print(e)
        raise ValueError