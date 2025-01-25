from configparser import ConfigParser
from functools import lru_cache

class Config():
    
    def __init__(self):
        self.config_route = '/etc/secrets/cfg.cfg'
        self.config = None
    
    @lru_cache
    def get_config(self):
        cfg_aux = ConfigParser()
        cfg_aux.read(self.config_route)
        self.config = cfg_aux
        return self.config
