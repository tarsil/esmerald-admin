import os
from functools import cached_property
from typing import Optional

from esmerald.conf.enums import EnvironmentType
from esmerald.conf.global_settings import EsmeraldAPISettings
from esmerald.config.jwt import JWTConfig
from saffier import Database, Registry


class AppSettings(EsmeraldAPISettings):
    app_name: str = "My application in production mode."
    title: str = "My project"
    environment: Optional[str] = EnvironmentType.PRODUCTION
    secret_key: str = "esmerald-insecure-)&amp;e5_#d@%z8h+p23r-6a8nhh!sc##^8x"

    @cached_property
    def db_access(self):
        database = Database(os.environ["SAFFIER_DATABASE_URL"])
        registry = Registry(database=database)
        return database, registry

    @property
    def jwt_config(self) -> JWTConfig:
        return JWTConfig(signing_key=self.secret_key)
