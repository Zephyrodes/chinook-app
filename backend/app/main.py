import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import routers as public_routers
from .routers import purchase as purchase_router

# Create DB tables on startup if env var allows (useful for dev; in prod use migrations)
CREATE_TABLES_ON_START = os.getenv("CREATE_TABLES_ON_START", "false").lower() == "true"

app = FastAPI(
    title="Chinook Sales API",
    description="API para compras de canciones y lectura del catálogo (FastAPI + MySQL).",
    version="1.0.0",
)

# CORS - ajusta orígenes según frontend (no dejar wildcard en producción si no es necesario)
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public_routers.router, prefix="/api", tags=["catalog"])
app.include_router(purchase_router.router, prefix="/api", tags=["purchase"])

@app.on_event("startup")
def startup_event():
    if CREATE_TABLES_ON_START:
        # solo en desarrollo; en producción usar alembic/migrations
        Base.metadata.create_all(bind=engine)
