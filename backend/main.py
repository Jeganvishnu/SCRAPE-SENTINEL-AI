from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger_config import logger
from app.api import health, sources, runs, failures, metrics, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Scrape Sentinel AI — Autonomous Self-Healing & AI Scraper Intelligence API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local frontend development
origins = [
    "*",
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router)
app.include_router(sources.router)
app.include_router(runs.router)
app.include_router(failures.router)
app.include_router(metrics.router)
app.include_router(ai.router)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI AI Scraper Intelligence Application Starting Up...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
