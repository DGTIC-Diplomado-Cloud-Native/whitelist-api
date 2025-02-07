from configparser import ConfigParser
from functools import lru_cache

class Config():
    '''
    Clase para manejar la configuración de la aplicación desde un archivo cfg.cfg.
    Utiliza lru_cache para mantener en memoria la configuración y evitar lecturas repetidas.
    '''
    
    def __init__(self):
        self.config_route = 'cfg.cfg'
        self.config = None
    
    @lru_cache
    def get_config(self):
        '''
        Obtiene la configuración del archivo cfg.cfg.
        '''
        cfg_aux = ConfigParser()
        cfg_aux.read(self.config_route)
        self.config = cfg_aux
        return self.config
