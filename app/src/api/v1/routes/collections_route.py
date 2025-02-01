import boto3

from fastapi import FastAPI
from fastapi import status
from typing import Dict, List

from app.src.api.services.collections_service import CollectionsService

app = FastAPI()
rekognition = boto3.client('rekognition')

@app.get('/collections',
         status_code=status.HTTP_200_OK,
         summary='Lista las colecciones actuales.')
async def list_collections() -> List[Dict]:
    service = CollectionsService
    return await service.list_collections()
