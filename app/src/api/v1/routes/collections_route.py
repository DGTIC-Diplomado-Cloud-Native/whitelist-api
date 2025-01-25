# app/main.py
import boto3

from fastapi import FastAPI, HTTPException
from botocore.exceptions import ClientError
from typing import Dict, List

app = FastAPI()
rekognition = boto3.client('rekognition')

@app.post("/collections/{collection_id}")
async def create_collection(collection_id: str) -> Dict:
    try:
        response = rekognition.create_collection(
            CollectionId=collection_id
        )
        return {
            "status": "success",
            "collection_id": collection_id,
            "face_model_version": response['FaceModelVersion'],
            "collection_arn": response['CollectionArn']
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            raise HTTPException(status_code=409, detail="Collection already exists")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections() -> Dict[str, List[str]]:
    try:
        response = rekognition.list_collections()
        return {"collections": response['CollectionIds']}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/collections/{collection_id}")
async def delete_collection(collection_id: str) -> Dict:
    try:
        rekognition.delete_collection(CollectionId=collection_id)
        return {"status": "success", "message": f"Collection {collection_id} deleted"}
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise HTTPException(status_code=404, detail="Collection not found")
        raise HTTPException(status_code=500, detail=str(e))
