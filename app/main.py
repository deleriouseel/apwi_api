from fastapi import FastAPI
from . import models
from .database import engine
from .routers import programs, networks


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(programs.router)
app.include_router(networks.router)


@app.get("/")
def read_root():
<<<<<<< Updated upstream
    return {"Hello World": "Jesus Loves You"}
=======
    return {"Hello World": "Jesus Loves You. See /docs for docs."}
>>>>>>> Stashed changes
