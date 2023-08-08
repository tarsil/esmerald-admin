from edgy import Database, Registry
from esmerald import Esmerald, EsmeraldAPISettings, Include
from esmerald.config.jwt import JWTConfig
from esmerald.contrib.auth.edgy.base_user import AbstractUser

from esmerald_admin import Admin
from esmerald_admin.backends.edgy.email import EmailAdminAuth

database = Database("sqlite:///db.sqlite")
registry = Registry(database=database)


class AppSettings(EsmeraldAPISettings):
    @property
    def jwt_config(self) -> JWTConfig:
        return JWTConfig(signing_key=self.secret_key)


class User(AbstractUser):
    """Inherits from the user base"""

    class Meta:
        registry = registry


# You can use the `settings_config` directly or ESMERALD_SETTINGS_MODULE
settings = AppSettings()


def get_application():
    """
    This is optional. The function is only used for organisation purposes.
    """

    app = Esmerald(
        routes=[Include(namespace="linezap.urls")],
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
        settings_config=settings,
    )

    # EmailAdminAuth or UsernameAdminAuth
    auth_backend = EmailAdminAuth(
        secret_key=settings.secret_key, auth_model=User, config=settings.jwt_config
    )
    Admin(app, registry.engine, authentication_backend=auth_backend)

    return app


app = get_application()
