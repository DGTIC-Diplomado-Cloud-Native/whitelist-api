from fastapi import APIRouter
from fastapi import status
from typing import Dict

from app.src.api.services.collections_service import CollectionsService

# Router from api.
router = APIRouter(prefix='/collections',
                   tags=['Collections'])

@router.get('/list-collections',
            status_code=status.HTTP_200_OK,
            summary='Lista las colecciones actuales.')
async def list_collections() -> Dict:
    '''
    Endpoint para listar todas las colecciones.
    '''
    service = CollectionsService()
    return await service.list_collections()

@router.post('/search-in-collection',
             status_code=status.HTTP_200_OK,
             summary='Busca coincidencias en una coleccion.')
async def search_in_collection(image_url: str) -> Dict:
    '''
    Endpoint para buscar coincidencias en una colección.
    '''
    service = CollectionsService()
    return await service.search_face_in_collection(collection_id='avengers-whitelist', image_url=image_url)
