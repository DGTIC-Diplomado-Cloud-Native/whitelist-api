import boto3
import os
import requests

from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.api.exceptions.custom_exceptions import ClientRekoError
from typing import Dict
from app.src.core.logging import configure_log
from dotenv import load_dotenv

# Logger
logger = configure_log()

# ENV
load_dotenv()

rekognition = boto3.client('rekognition',
                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                           aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                           region_name='us-east-2')

class CollectionsService():
    '''
    Capa de servicio para gestionar las operaciones de colecciones.
    '''
    
    def __init__(self, session: AsyncSession = None):
        self.repository = None
        
    async def list_collections(self) -> Dict:
        '''
        Lista las colecciones actuales de AWS Reko.
        '''
        try:
            response = rekognition.list_collections()
            return response
        except Exception as err:
            logger.error(f'Ocurrió un error al listar las colecciones: {err}')
            raise ClientRekoError(message='Ocurrió un error al listar las colecciones.')
        
    async def create_face_collection(self, collection_id):
        '''
        Crea una nueva colección de rostros en AWS Rekognition
        '''
        try:
            response = rekognition.create_collection(CollectionId=collection_id)
            
            if response['StatusCode'] == 200:
                logger.info(f"Colección '{collection_id}' creada exitosamente!")
                logger.info(f"ARN: {response['CollectionArn']}")
                return response
        except Exception as e:
            logger.error(f"Error al crear colección: {str(e)}")
            raise ClientRekoError(message=f"Error al crear colección: {str(e)}")
        
    async def add_face_to_collection(self, collection_id, image_path, external_image_id=None):
        """
        Agrega un rostro a una colección desde una imagen local
        """
        try:
            # Leer imagen en bytes
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

            # Llamar a Rekognition
            response = rekognition.index_faces(
                CollectionId=collection_id,
                Image={'Bytes': image_bytes},
                ExternalImageId=external_image_id or os.path.basename(image_path),
                DetectionAttributes=['ALL']
            )

            # Procesar respuesta
            if response['FaceRecords']:
                logger.info(f"Rostro agregado desde {image_path}")
                logger.info(f"Face ID: {response['FaceRecords'][0]['Face']['FaceId']}")
                return response
            else:
                logger.warn(f"No se detectaron rostros en {image_path}")
                return None

        except Exception as e:
            logger.error(f"Error procesando {image_path}: {str(e)}")
            raise ClientRekoError(message=f"Error procesando {image_path}: {str(e)}")
        
    async def search_face_in_collection(self, collection_id, image_url, threshold=90):
        """
        Busca un rostro en la colección usando una imagen desde una URL
        """
        try:
            
            result = {'ID Externo': None, 'Confianza': None, 'Face ID': None}
            
            # Descargar imagen desde la URL
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Convertir a bytes
            image_bytes = BytesIO(response.content).read()

            # Buscar en la colección
            search_response = rekognition.search_faces_by_image(
                CollectionId=collection_id,
                Image={'Bytes': image_bytes},
                FaceMatchThreshold=threshold,
                MaxFaces=5
            )

            # Procesar resultados
            matches = []
            for face_match in search_response.get('FaceMatches', []):
                match_data = {
                    'FaceId': face_match['Face']['FaceId'],
                    'ExternalImageId': face_match['Face'].get('ExternalImageId', 'N/A'),
                    'Confidence': face_match['Similarity'],
                    'BoundingBox': face_match['Face']['BoundingBox']
                }
                matches.append(match_data)

            if len(matches) > 0:
                for match in matches:
                    result['ID Externo'] = match['ExternalImageId']
                    result['Confianza'] = f"{match['Confidence']:.2f}%"
                    result['Face ID'] = match['FaceId']
                    
            return result

        except Exception as e:
            logger.error(f"Error en la búsqueda: {str(e)}")
            raise ClientRekoError(message=f"Error en la búsqueda: {str(e)}")
