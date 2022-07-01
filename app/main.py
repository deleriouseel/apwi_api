from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from pydantic import Required, BaseModel  

from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine
from .routers import programs, networks


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(programs.router)
app.include_router(networks.router)

#root 
@app.get("/")
def read_root():
    return {"Hello": "World"}

