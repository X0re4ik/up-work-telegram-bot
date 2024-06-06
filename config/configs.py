from dotenv import load_dotenv
from typing import Optional

import abc
import os

class ABCConfig(abc.ABC):

    PREFIX: str = ""

    def from_env(self, key, *, use_prefix: bool = True, default=None):
        key_ = key if not use_prefix else self.PREFIX + "_" + key
        return os.getenv(key_, default)

class ConfigTelegram(ABCConfig):
    
    PREFIX = "TELEGRAM"
    
    @property
    def TOKEN(self):
        return self.from_env("TOKEN")
    

class ConfigRAMStorage(ABCConfig): 
    
    @property
    def LOGIN(self):
        return self.from_env("LOGIN", default=None)
    
    @property
    def PASSWORD(self):
        return self.from_env("PASSWORD", default=None)
    
    @property
    def HOST(self):
        return self.from_env("HOST")
    
    @property
    def PORT(self):
        return self.from_env("PORT")
    
    def is_public(self):
        return self.LOGIN is None and self.PASSWORD is None
    
    @property
    @abc.abstractmethod
    def URL(self):
        raise NotImplementedError()
    
class APIService(ABCConfig):
    
    PREFIX = "BACKEND_API"
    
    @property
    def HOST(self):
        return self.from_env("HOST")
    
    @property
    def PORT(self):
        return self.from_env("PORT")
    
    @property
    def PROTOCOL(self):
        return self.from_env("PROTOCOL")
    
    @property
    def DEFAULT_PATH(self):
        return self.from_env("DEFAULT_PATH")
    
    @property
    def URL(self):
        return "{}://{}:{}/{}/".format(
            self.PROTOCOL, 
            self.HOST, 
            self.PORT,
            self.DEFAULT_PATH
        )
    

class ConfigRedis(ConfigRAMStorage):
    PREFIX = "REDIS"
    
    @property
    def URL(self):
        prefix = ""
        if not self.is_public():
            prefix = "{}:{}@".format(self.LOGIN, self.PASSWORD)
        return f"redis://{prefix}{self.HOST}:{self.PORT}/0"
    

redis_config = ConfigRedis()
telegram_config = ConfigTelegram()

api_service = APIService()