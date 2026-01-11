from fastapi import APIRouter

from App.Api.ordenes_trabajo import router as ordenes_trabajo_router

api_router = APIRouter()
api_router.include_router(
    ordenes_trabajo_router,
    prefix="/ordenes_trabajo",
    tags=["ordenes_trabajo"],
)
