from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


import debugpy
debugpy.listen(("0.0.0.0", 5678))


@app.get("/")
def root():    
    return {"message": "Hello World"}