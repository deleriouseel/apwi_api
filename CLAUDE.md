# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

FastAPI + PostgreSQL read-mostly API serving the "Apply Within" radio program archive: broadcast episodes (`apwi` table), the radio stations that air them, station locations, and airtimes. A React frontend (`apwi_front`, separate repo) consumes it. Deployed to Azure App Service via GitHub Actions on push to `main`.

## Commands

Windows dev uses the checked-out `venv/`:

```powershell
venv\Scripts\activate
pip install -r requirements-dev.txt  # runtime + test/lint deps (-r's requirements.txt)
uvicorn app.main:app --reload        # dev server on :8000
pytest                               # full suite
pytest tests/test_programs.py::test_program -v   # single test
alembic upgrade head                 # apply migrations
alembic revision --autogenerate -m "describe change"
python seed_stations.py --dry-run    # preview station seed; drop the flag to write
```

There is no linter or formatter wired into CI. `.vscode/settings.json` sets black as the Python formatter and enables pylint.

### Two requirements files

`requirements.txt` is **runtime only** — it is what the Azure workflows install, so it defines the production image. `requirements-dev.txt` starts with `-r requirements.txt` and adds pytest, pylint/isort, and selenium plus their transitive deps. Anything imported under `app/` must go in `requirements.txt`; test- and lint-only packages must not, or they ship to production and widen the dependency-vulnerability surface for no benefit.

Requires a `.env` at the repo root with `DATABASE_HOSTNAME`, `DATABASE_PORT`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_NAME`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and optionally `CORS_ALLOW_ORIGINS`. [app/config.py](app/config.py) fails at import time if any required key is missing — every command above, including `pytest` and `alembic`, needs it.

## Testing caveat

[tests/test_programs.py](tests/test_programs.py) runs `TestClient` against the **real configured database**, not a fixture DB. Tests assert on live row counts and on today's date (`test_program` expects the newest program's airdate to equal today), so they fail if the DB isn't current or reachable. There is no test DB setup, no fixtures, and no auth coverage — writing tests for new endpoints means deciding on that infrastructure first.

## Architecture

Standard FastAPI layering, all under [app/](app/):

- [main.py](app/main.py) — app assembly, CORS, router registration, `openapi_tags` list that controls `/docs` section order, and the `/admin` route.
- [models.py](app/models.py) — SQLAlchemy ORM. `STATION` ↔ `LOCATION` and `STATION` ↔ `AIRTIME` are many-to-many via the `station_location` / `station_airtime` junction tables.
- [schemas.py](app/schemas.py) — Pydantic v2. Response models (`*Base`), create models (`*Create`), and PATCH models (`*Update`, all fields optional).
- [routers/](app/routers/) — one module per resource, all mounted under `/v1`.
- [oauth2.py](app/oauth2.py) / [utils.py](app/utils.py) — JWT issue/verify and bcrypt password hashing.

### Router registration order matters

[networks.py](app/routers/networks.py) declares catch-all paths `/v1/{network}` and `/v1/{network}/{start_date}`. It is registered **last** in `main.py` so that `/v1/stations`, `/v1/programs`, `/v1/locations`, etc. match first. Adding a new `/v1/<name>` router means registering it before `networks`, or it will be swallowed by the network route.

### Auth model

Reads are public; every POST/PATCH/DELETE takes `current_user: int = Depends(oauth2.get_current_user)`. `get_current_user` must return a real user or raise — it explicitly rejects validly-signed tokens whose user row has been deleted, because returning `None` would let routes run unauthenticated. `/v1/users` routes are `include_in_schema=False` (hidden from `/docs`) and creating a user itself requires an existing token, so the first user is provisioned directly in the DB.

### Naming quirks that trip up edits

- The station column is `callletters` (no underscore) but the API exposes `call_letters`. `StationBase` maps it with `validation_alias="callletters"`; `StationCreate` uses `serialization_alias` and the POST route calls `model_dump(by_alias=True)`; `patch_station` translates the field name by hand. Touching any one of these three requires checking the others.
- `APWI.airdate` is a **String** column, not Date, so date filtering is lexicographic on `YYYY-MM-DD` strings and `patch_program` converts the parsed `date` back with `.isoformat()`.
- Primary keys are inconsistent: `idStation`, `idLocation`, `idAirtime`, but plain `id` on `apwi` and `users`.
- Empty result sets raise **400**, not 404 or an empty list, across the list endpoints. Existing frontend behavior depends on this.

### PATCH convention

Every PATCH route follows the same shape: fetch-or-404 via a module-level `_get_*_or_404` helper, `model_dump(exclude_unset=True)` so omitted fields aren't nulled, 400 if the body is empty, then `setattr` per field. Match this when adding update routes.

### Migrations

Alembic reads the DB URL from `app.config.settings` in [alembic/env.py](alembic/env.py), so `alembic.ini` carries no credentials. Note that `main.py` also calls `models.Base.metadata.create_all()` at startup — this creates missing tables but never alters existing ones, so schema changes still need a real migration. Current head is `a1b2c3d4e5f6`.

### Admin UI

[app/static/admin.html](app/static/admin.html) is a single self-contained page served at `/admin` from the same origin (avoiding CORS). It logs in against `/v1/login`, holds the bearer token in memory only, and drives the same public REST endpoints — no separate admin API exists.

## Stray file

[app/test.py](app/test.py) is an untracked five-line fragment, not a module — it references undefined names and is not imported anywhere. Don't treat it as part of the app.
