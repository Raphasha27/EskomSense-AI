from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="EskomSense AI",
    description="ML-powered load shedding prediction for South Africa",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.middleware("http")
async def add_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Powered-By"] = "Kirov Dynamics"
    response.headers["X-Trial"] = "true"
    return response


static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(str(static_dir / "index.html"))
