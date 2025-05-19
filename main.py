# main.py (w głównym katalogu)
from fastapi import FastAPI
from backend.controllers.reading_controller import router as reading_router

app = FastAPI()
app.include_router(reading_router)
