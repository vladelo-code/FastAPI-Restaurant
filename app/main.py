from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title='FastAPI-Restaurant', description='Made by Vladislav Lahtionov')

app.include_router(api_router, prefix="/api")
