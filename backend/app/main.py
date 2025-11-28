import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import routers as public_routers        # <- cambio a import absoluto
from app.routers import purchase as purchase_router      # <- cambio a import absoluto

CREATE_TABLES_ON_START = os.getenv("CREATE_TABLES_ON_START", "false").lower() == "true"

app = FastAPI(
    title="Chinook Sales API",
    description="API para compras de canciones y lectura del catálogo (FastAPI + MySQL).",
    version="1.0.0",
)

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(public_routers.router, prefix="/api", tags=["catalog"])
app.include_router(purchase_router.router, prefix="/api", tags=["purchase"])

@app.on_event("startup")
def startup_event():
    if CREATE_TABLES_ON_START:
        # Solo en dev; en prod usar migraciones
        Base.metadata.create_all(bind=engine)
