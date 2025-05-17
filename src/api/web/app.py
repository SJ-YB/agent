from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, FastAPI

from src.api.web.router.default import router as default_router
from src.container import Container
from src.settings import ServiceName


def _build_router(service_name: str) -> APIRouter:
    router = APIRouter()
    api_router = APIRouter(prefix="/api")
    match service_name:
        case ServiceName.SIMPLE_CHAT:
            from src.api.web.router.chat import router as service_router
        case _:
            raise ValueError(f"Unknown Service Name. {service_name}")
    api_router.include_router(service_router)
    router.include_router(api_router)
    router.include_router(default_router)

    return router


@inject
def create_web_app(
    service_name: str = Provide[Container.env_config.service_name],
) -> FastAPI:
    app = FastAPI()
    router = _build_router(service_name)
    app.include_router(router)

    return app
