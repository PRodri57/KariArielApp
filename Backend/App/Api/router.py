from fastapi import APIRouter

from App.Api.clientes import router as clientes_router
from App.Api.ordenes_trabajo import router as ordenes_trabajo_router
from App.Api.telefonos import router as telefonos_router

api_router = APIRouter()
api_router.include_router(
    clientes_router,
    prefix="/clientes",
    tags=["clientes"],
)
api_router.include_router(
    telefonos_router,
    prefix="/telefonos",
    tags=["telefonos"],
)
api_router.include_router(
    ordenes_trabajo_router,
    prefix="/ordenes_trabajo",
    tags=["ordenes_trabajo"],
)
