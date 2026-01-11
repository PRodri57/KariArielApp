import os

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from App.Api.router import api_router
from App.db.errors import DatabaseUnavailableError

DEFAULT_CORS_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


def cors_config_from_env() -> tuple[list[str], str | None]:
    raw = os.getenv("CORS_ORIGINS", "").strip()
    if not raw:
        return list(DEFAULT_CORS_ORIGINS), None
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    if "*" in origins:
        return [], ".*"
    return origins or list(DEFAULT_CORS_ORIGINS), None


app = FastAPI(title="KariAriel App")
cors_origins, cors_origin_regex = cors_config_from_env()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.exception_handler(DatabaseUnavailableError)
def database_unavailable_handler(
    request: Request, exc: DatabaseUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": exc.detail},
    )
