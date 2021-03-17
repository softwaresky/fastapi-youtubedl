from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from app.api.api_v1.api import api_router
from app.core.config import settings
import os

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

folder = "C:/Users/Softwaresky/PycharmProjects/fastapi-youtubedl/frontend/dist"
app.mount("/static", StaticFiles(directory=folder), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = f'{folder}/index.html'
    return FileResponse(path)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print ("custom_http_exception_handler() ....")
    return RedirectResponse("/")