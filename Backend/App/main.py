from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from App.Api.router import api_router
from App.db.errors import DatabaseUnavailableError

app = FastAPI(title="KariAriel App")
app.include_router(api_router)


@app.exception_handler(DatabaseUnavailableError)
def database_unavailable_handler(
    request: Request, exc: DatabaseUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": exc.detail},
    )
