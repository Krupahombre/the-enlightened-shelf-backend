import logging

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.server.routers.book_router import router as book_router
from src.server.routers.auth_router import router as auth_router
from src.server.routers.user_router import router as user_router
from src.utils.config_provider import config_provider


class Server:
    def __init__(self):
        self.logger = logging.getLogger("Server")
        docs = "/docs" if int(config_provider.get_config_value("server", "docs")) else None
        redoc = "/redoc" if int(config_provider.get_config_value("server", "redoc")) else None
        allow_origins = config_provider.get_config_value("server", "allow_origins").split(",")
        allow_methods = config_provider.get_config_value("server", "allow_methods").split(",")
        allow_headers = config_provider.get_config_value("server", "allow_headers").split(",")
        self.prefix = config_provider.get_config_value("server", "prefix")
        self.app = FastAPI(docs_url=docs, redoc_url=redoc)
        self.app.add_middleware(CORSMiddleware, allow_origins=allow_origins, allow_methods=allow_methods,
                                allow_headers=allow_headers)
        self.routers = [user_router, auth_router, book_router]

    def prepare_routers(self):
        for router in self.routers:
            self.include_router(router, self.prefix)

    def include_router(self, router: APIRouter, prefix: str = "/api/v1"):
        self.app.include_router(router=router, prefix=prefix)
