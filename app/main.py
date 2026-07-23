from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from . import models
from .config import settings
from .database import engine
from .routers import programs, networks, stations, users, login, locations

STATIC_DIR = Path(__file__).parent / "static"


models.Base.metadata.create_all(bind=engine)

# Controls the section order in /docs and /redoc. Tags not listed here fall to
# the bottom; "default" holds any untagged route (currently GET /).
openapi_tags = [
    {"name": "Apply Within Programs"},
    {"name": "Apply Within Programs by Network"},
    {"name": "Apply Within Radio Stations"},
    {"name": "Radio Station Locations"},
    {"name": "Login"},
    {"name": "default"},
]

app = FastAPI(openapi_tags=openapi_tags)

# "*" and allow_credentials=True are mutually exclusive under the CORS spec --
# browsers reject the combination. Auth here uses a Bearer header rather than
# cookies, so credentialed CORS is only enabled when real origins are listed.
cors_origins = settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(locations.router)
app.include_router(stations.router)
app.include_router(programs.router)
app.include_router(networks.router)


@app.get("/")
def read_root():
    return {
        "Hello World": "Jesus Loves You. See /docs for docs. Or /redoc if that's how you roll."
    }


@app.get("/admin", include_in_schema=False)
def admin_page():
    # Simple browser UI for managing the DB. Served from the same origin as the
    # API so its logged-in fetch() calls don't hit CORS. Auth still happens
    # server-side -- this page just holds the bearer token in memory.
    return FileResponse(STATIC_DIR / "admin.html")
