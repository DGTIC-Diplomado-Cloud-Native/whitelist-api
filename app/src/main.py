from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware

from app.src.core.logging import configure_log
from app.src.core.config import Config

from app.src.api.exceptions.custom_exceptions import APIException

from app.src.api.v1.routes import collections_route

@dataclass
class AppFactory:
    '''
    Factory para crear y configurar la aplicación FastAPI.
    '''

    config: Dict[str, Any]
    logger = configure_log()

    def create_app(self) -> FastAPI:
        app = FastAPI(
            title='Collections API',
            description='AWS Reko Collections Admin API',
            version='1.0',
            docs_url='/api/docs',
            redoc_url='/api/redoc',
            openapi_url='/api/openapi.json',
            root_path='/v1'
        )
        
        self._configure(app)
        return app

    def _configure(self, app: FastAPI) -> None:
        """Configura middlewares, manejadores de errores y rutas."""
        self._add_middlewares(app)
        self._add_exception_handlers(app)
        self._add_routes(app)

    def _add_middlewares(self, app: FastAPI) -> None:
        app.add_middleware(
            GZipMiddleware,
            minimum_size=1000
        )
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    def _add_exception_handlers(self, app: FastAPI) -> None:
        async def handle_api_exception(request: Request, exc: APIException) -> JSONResponse:
            self.logger.exception(
                f"handle_api_exception: {exc.message}",
                extra={
                    "trace_id": exc.trace_id,
                    "path": request.url.path,
                    "method": request.method,
                    "error_code": exc.error_code
                }
            )
            
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "message": exc.message,
                    "error_code": exc.error_code,
                    "timestamp": exc.timestamp.isoformat(),
                    "trace_id": exc.trace_id,
                    "path": request.url.path
                }
            )

        async def handle_global_exception(request: Request, exc: Exception) -> JSONResponse:
            trace_id = str(uuid4())
            self.logger.critical(
                f'Unhandled error: {str(exc)}',
                exc_info=True,
                extra={'trace_id': trace_id}
            )
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "An unexpected error occurred",
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "trace_id": trace_id,
                    "timestamp": datetime.now().isoformat()
                }
            )

        app.add_exception_handler(APIException, handle_api_exception)
        app.add_exception_handler(Exception, handle_global_exception)

    def _add_routes(self, app: FastAPI) -> None:
        app.include_router(collections_route.router)

def create_app() -> FastAPI:
    return AppFactory(Config().get_config()).create_app()

app = create_app()
