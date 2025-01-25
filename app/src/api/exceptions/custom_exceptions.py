from fastapi import status
from datetime import datetime
from uuid import uuid4

class APIException(Exception):
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
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code='RESOURCE_NOT_FOUND'
        )

class ValidationError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code='VALIDATION_ERROR'
        )
        
class DatabaseError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='DATABASE_ERROR'
        )
        
class AuthenticationError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code='AUTHENTICATION_ERROR'
        )
        
class AuthorizationError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code='AUTHORIZATION_ERROR'
        )
        
class GenerateValidFileParamsError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='GENERATE_VALID_FILE_PARAMS_ERROR'
        )

class InsertInfoExperimentError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='INSERT_INFO_EXPERIMENT_ERROR'
        )
        
class GenerateValidFileMasiveError(APIException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code='GENERATE_VALID_FILE_MASIVE_ERROR'
        )
