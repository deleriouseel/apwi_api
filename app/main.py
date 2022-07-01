from fastapi import FastAPI
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

