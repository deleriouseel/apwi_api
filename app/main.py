from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import programs, networks


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

#why is CORS not working now?

app.include_router(programs.router)
app.include_router(networks.router)


@app.get("/")
def read_root():
    return {"Hello World": "Jesus Loves You. See /docs for docs."}
