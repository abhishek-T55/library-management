import logging
from fastapi import FastAPI
# from fastapi.routing import APIRoute

from app.core.config import config
from app.api.v1.main import api_router

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=config.project_name,
)

app.include_router(api_router)
