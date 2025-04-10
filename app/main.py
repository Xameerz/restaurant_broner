from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tables, reservations
from app.database import Base, engine
from app.core.logger import app_logger

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Booking API",
    description="API для управления бронированием столов в ресторане",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(tables.router, prefix="/api")
app.include_router(reservations.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    app_logger.info("Starting Restaurant Booking API")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Shutting down Restaurant Booking API")

@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Проверка работоспособности API
    """
    app_logger.info("Health check requested")
    return {"status": "ok"}
