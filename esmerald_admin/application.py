from typing import Optional, Sequence

from esmerald import Esmerald
from sqladmin import Admin as SQLAdmin
from sqladmin import ModelView as ModelView  # noqa
from sqladmin._types import ENGINE_TYPE
from sqladmin.authentication import AuthenticationBackend
from starlette.middleware import Middleware


class Admin(SQLAdmin):
    """
    Tha base inherited for Saffier which inherits from the base of sqladmin package.
    """

    def __init__(
        self,
        app: Esmerald,
        engine: ENGINE_TYPE,
        base_url: str = "/admin",
        title: str = "Admin",
        logo_url: Optional[str] = None,
        middlewares: Optional[Sequence[Middleware]] = None,
        debug: bool = False,
        templates_dir: str = "templates",
        authentication_backend: Optional[AuthenticationBackend] = None,
    ) -> None:
        super().__init__(
            app,
            engine,
            base_url,
            title,
            logo_url,
            middlewares,
            debug,
            templates_dir,
            authentication_backend,
        )

        self.app.router.activate()  # type: ignore
