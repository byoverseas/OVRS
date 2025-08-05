from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.core.logger import logger
from app.routes import analytics, auth, listening, tasks

app = FastAPI(title="Secure FastAPI Skeleton")

origins = [orig.strip() for orig in settings.allowed_origins.split(',')] if settings.allowed_origins else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("startup complete", env=settings.env)


app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(analytics.router)
app.include_router(listening.router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code in {400, 401, 403}:
        detail = exc.detail if isinstance(exc.detail, str) else "Unauthorized"
        return JSONResponse(status_code=exc.status_code, content={"detail": detail})
    return JSONResponse(status_code=exc.status_code, content={"detail": "An error occurred"})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"})
