from fastapi import APIRouter

from app.api.api_v1.endpoints import ydl_item

api_router = APIRouter()
api_router.include_router(ydl_item.router, prefix="/youtube-dl", tags=["ydl_item"])