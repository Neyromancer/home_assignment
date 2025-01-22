from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.routers.application import router as application_router
from app.config import config
from app.database import sessionmanager

def init_app(init_db=True) -> FastAPI:
    lifespan = None
    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        # TODO: what is this for?
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager.engine:
                await sessionmanager.close()

    app = FastAPI(title="BeWise HomeAssignment", lifespan=lifespan)

    @app.get("/")
    async def root():
        return {"message": "BeWise HomeAssignment"}

    app.include_router(application_router)
    return app