from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse, HTMLResponse, FileResponse
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_methods="*")

app.include_router(api_router, prefix=settings.API_V1_STR)

if settings.STATIC_FOLDER:
    folder = settings.STATIC_FOLDER
    app.mount("/static", StaticFiles(directory=folder), name="static")

    @app.get("/", response_class=FileResponse)
    def root():
        path = f'{folder}/index.html'
        return FileResponse(path, media_type='text/html')