from fastapi import APIRouter

from app.api.v1.endpoints import users, login, books

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(books.router, prefix="/books", tags=["Books"])