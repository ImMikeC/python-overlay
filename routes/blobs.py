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
async def overlay_images(container: str, file1: str, file2: str, x: int, y: int, output: str):
    try:
        # conexion al Azure Blob storage
       
        blob_client_file1 = blob_service_client.get_blob_client(container=container, blob=file1)
        # obtener container

        # blob para imagen 1
        # Read the first image and save it as a numpy array

        # image1 = cv2.imdecode(
        #     np.asarray(bytearray(blob_client_file1.download_blob().readall()), dtype=np.uint8),
        #     cv2.IMREAD_COLOR
        # )
        image1 = Image.open(io.BytesIO(blob_client_file1.download_blob().readall()))


        # blob para imagen 2
        blob_client_file2 = blob_service_client.get_blob_client(container=container, blob=file2)

        # Read the second image and save it as a numpy array
        # image2 = cv2.imdecode(
        #     np.asarray(bytearray(blob_client_file2.download_blob().readall()), dtype=np.uint8),
        #     cv2.IMREAD_COLOR
        # )
        image2 = Image.open(io.BytesIO(blob_client_file2.download_blob().readall()))

        # ajusta tamano de la imagen 2 al tamano de la imagen 1
        # image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        # predefine alpha y beta
        # alpha = 0.5
        # beta = 1 - alpha
        
        # overlay usando cv2.addWeighted()
        # overlay = cv2.addWeighted(image1, alpha, image2, beta, 0)
        
        # comprime imagen antes de subirla al Azure Blob storage
        # _, img_encoded = cv2.imencode('.jpg', overlay)
        # img_bytes = img_encoded.tobytes()

        result = Image.new(image1.mode, image1.size)

        result.paste(image1)

        result.paste(image2, (x,y), mask = image2)

        img_bytes = io.BytesIO()
        result.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        upload_blob(output + '.jpeg', container, data = img_bytes)

        return {"message": "Overlay image uploaded to Azure Blob storage successfully."}
    except Exception as e:
        return {"error": str(e)}