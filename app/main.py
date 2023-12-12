from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import programs, networks, stations, users, login


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(programs.router)
app.include_router(networks.router)
app.include_router(stations.router)
app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
def read_root():
    return {
        "Hello World": "Jesus Loves You. See /docs for docs. Or /redoc if that's how you roll."
    }
