from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from routers import purchase
app = FastAPI(title="Chinook API")
app.include_router(purchase.router)
@app.get("/")
async def root():
    return {"message":"Chinook FastAPI running"}
