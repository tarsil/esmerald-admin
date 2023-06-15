from functools import cached_property
from typing import Optional

from esmerald.conf.enums import EnvironmentType
from esmerald.conf.global_settings import EsmeraldAPISettings
from saffier import Database, Registry


class AppSettings(EsmeraldAPISettings):
    app_name: str = "My application in production mode."
    title: str = "My linezap"
    environment: Optional[str] = EnvironmentType.PRODUCTION
    secret_key: str = "esmerald-insecure-key"

    @cached_property
    def db_access(self):
        database = Database("sqlite:///db.sqlite")
        registry = Registry(database=database)
        return database, registry
