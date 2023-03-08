from fastapi import FastAPI
from api.views import note_router

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

app.include_router(note_router, prefix="/api")