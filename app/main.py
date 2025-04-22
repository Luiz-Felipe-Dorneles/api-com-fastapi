from fastapi import FastAPI
from route import series

app = FastAPI()

app.include_router(series.router)