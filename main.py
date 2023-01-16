from fastapi import FastAPI
from routes.blobs import blob_routes

app = FastAPI()
app.include_router(blob_routes, prefix="/storage/blob")