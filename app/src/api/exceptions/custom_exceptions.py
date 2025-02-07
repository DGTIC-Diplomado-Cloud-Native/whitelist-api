from fastapi import status
from datetime import datetime
from uuid import uuid4

class APIException(Exception):
    '''
    Clase base para excepciones personalizadas de la API.
    Incluye mensaje, código de estado HTTP, código de error, timestamp y ID de rastreo.
    '''
    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.timestamp = datetime.now()
        self.trace_id = str(uuid4())

class NotFoundError(APIException):
    '''
    Excepción para recursos no encontrados.
    Código estado: 404 Not Found.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code='RESOURCE_NOT_FOUND'
        )

class ValidationError(APIException):
    '''
    Excepción para errores de validación de datos.
    Código estado: 422 Unprocessable Entity.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code='VALIDATION_ERROR'
        )
        
class DatabaseError(APIException):
    '''
    Excepción para errores de base de datos.
    Código estado: 500 Internal Server Error.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='DATABASE_ERROR'
        )
        
class AuthenticationError(APIException):
    '''
    Excepción para errores de autenticación.
    Código estado: 401 Unauthorized.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code='AUTHENTICATION_ERROR'
        )
        
class AuthorizationError(APIException):
    '''
    Excepción para errores de autorización.
    Código estado: 403 Forbidden.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code='AUTHORIZATION_ERROR'
        )
        
class GenerateValidFileParamsError(APIException):
    '''
    Excepción para errores en la generación de parámetros de archivo.
    Código estado: 500 Internal Server Error.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='GENERATE_VALID_FILE_PARAMS_ERROR'
        )

class ClientRekoError(APIException):
    '''
    Excepción para errores del cliente Rekognition.
    Código estado: 500 Internal Server Error.
    '''
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='CLIENT_REKO_ERROR'
        )
