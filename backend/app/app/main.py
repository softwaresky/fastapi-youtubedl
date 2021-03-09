from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.api_v1.api import api_router
from app.core.config import settings

# app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)

# Mounting default Vue files after running npm run build
app.mount("/dist", StaticFiles(directory="/vue/dist/"), name="dist")
app.mount("/css", StaticFiles(directory="/vue/dist/css"), name="css")
app.mount("/fonts", StaticFiles(directory="/vue/dist/fonts"), name="fonts")
# app.mount("/img", StaticFiles(directory="/vue/dist/img"), name="img")
app.mount("/js", StaticFiles(directory="/vue/dist/js"), name="js")

# app.mount("/static", StaticFiles(directory="/vue/dist"), name="static")

templates = Jinja2Templates(directory="/vue/dist")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})