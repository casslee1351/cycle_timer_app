from fastapi import FastAPI
from app.config import settings
from app.routers import cycles

app = FastAPI(title=settings.app_name)
app.include_router(cycles.router)

@app.get("/")
def read_root():
    return {"message": f"{settings.app_name} is running"}