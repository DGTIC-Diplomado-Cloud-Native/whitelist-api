import boto3

from sqlalchemy.ext.asyncio import AsyncSession
from app.src.api.exceptions.custom_exceptions import ClientRekoError
from typing import Dict
from app.src.core.logging import configure_log

# Logger
logger = configure_log()

rekognition = boto3.client('rekognition',
                           aws_access_key_id='AKIA6KQKJUMKRJ546N6Q',
                           aws_secret_access_key='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',
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

if __name__ == '__main__':
    import asyncio
    
    async def main():
        service = CollectionsService()
        res = await service.list_collections()
        print(res)
    
    asyncio.run(main=main())
