from fastapi import APIRouter, Form, UploadFile, File
from azure_blob_functions.blob import get_blob, upload_blob, download_blob, delete_blob
import cv2
import numpy as np
from PIL import Image
import io
from azure_blob_functions.blob import blob_service_client

blob_routes = APIRouter()

@blob_routes.post("/upload")
async def upload(container: str = Form(...), file: UploadFile = File(...)):
    data = await file.read()
    filename = file.filename
    return upload_blob(filename, container, data)

@blob_routes.get("/file/{container}/{filename}")
def get_file(container: str, filename: str):
    return get_blob(filename, container)



@blob_routes.get("/download/{container}/{filename}")
def download_file(container: str, filename: str):
    return download_blob(filename, container)

@blob_routes.delete("/delete")
def delete_file(container: str = Form(...), filename: str = Form(...)):
    return delete_blob(filename, container)

@blob_routes.post("/overlay")
async def overlay_images(container: str, file1: str, file2: str, width: int, height: int, x: int, y: int, output: str):
    try:
       # conexion al Azure Blob storage en azure_blob_functions/blobs.py
       
       # blob para imagen 1
        blob_client_file1 = blob_service_client.get_blob_client(container=container, blob=file1)
        image1 = Image.open(io.BytesIO(blob_client_file1.download_blob().readall()))

        # blob para imagen 2
        blob_client_file2 = blob_service_client.get_blob_client(container=container, blob=file2)
        image2 = Image.open(io.BytesIO(blob_client_file2.download_blob().readall()))
        # Se ajusta tamaño de la imagen de acuerdo al input
        image2 = image2.resize((height, width))

        # Se crea imagen con las mismas caracteristicas que la imagen 1.
        result = Image.new(image1.mode, image1.size)

        result.paste(image1)
        # x para posicion horizontal e y para posicion vertical
        result.paste(image2, (x,y), mask = image2)

        # Guardar result() como objeto binario
        img_bytes = io.BytesIO()
        result.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        upload_blob(output + '.jpeg', container, data = img_bytes)

        return {"message": "Overlay image uploaded to Azure Blob storage successfully."}
    except Exception as e:
        return {"error": str(e)}