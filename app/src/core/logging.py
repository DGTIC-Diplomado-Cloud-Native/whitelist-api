import os

from typing import Optional
from loguru import logger
from dataclasses import dataclass
from pathlib import Path
from app.src.core.config import Config

@dataclass
class LogConfig:
    '''
    Configuración para el logger
    '''
    file_path: Path
    max_size: int = 50 * 1024 * 1024  # 50MB en bytes
    backup_count: int = 15
    compression: str = "zip"
    level: str = "TRACE"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

class Logger:
    '''
    Clase para manejar la configuración y gestión del logger.
    '''
    _instance: Optional[any] = None
    
    def __init__(self, config: LogConfig) -> None:
        '''
        Inicializa el TLDLogger con la configuración proporcionada.
        
        Args:
            config (LogConfig): Configuración para el logger
        '''
        self._config = config
    
    def configure(self) -> any:
        '''
        Configura y devuelve un logger con rotación de archivos y copias de respaldo.
        '''
        # Crear directorio de logs si no existe
        os.makedirs(self._config.file_path.parent, exist_ok=True)
        
        # Limpiar configuraciones previas
        logger.remove()
        
        # Configurar el nuevo logger
        logger.add(sink=str(self._config.file_path),
                   rotation=self._config.max_size,
                   retention=self._config.backup_count,
                   compression=self._config.compression,
                   level=self._config.level,
                   format=self._config.format,
                   backtrace=True,
                   diagnose=True)
        
        Logger._instance = logger
        return logger
    
    @classmethod
    def get_instance(cls, config: LogConfig) -> any:
        '''
        Obtiene o crea una instancia única del logger (patrón Singleton).
        '''
        if cls._instance is None:
            logger_instance = cls(config)
            return logger_instance.configure()
        return cls._instance

def configure_log() -> any:
    '''
    Función helper para configurar el logger.
    '''
    cfg = Config().get_config()
    
    log_config = LogConfig(file_path=Path(cfg.get('API', 'LOG_PATH')))
    return Logger.get_instance(log_config)
