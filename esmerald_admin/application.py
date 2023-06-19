from typing import Optional, Sequence

from esmerald import Esmerald, HTTPException, Request, status
from esmerald.exceptions import ImproperlyConfigured
from sqladmin import Admin as SQLAdmin  # noqa
from sqladmin import ModelView as SQLAModelView  # noqa
from sqladmin._types import ENGINE_TYPE
from sqladmin.authentication import AuthenticationBackend
from sqladmin.models import BaseView as SQLAdminBaseView  # noqa
from starlette.middleware import Middleware


class EsmeraldBase:
    def is_accessible(self, request: Request) -> bool:  # type: ignore
        raise ImproperlyConfigured(
            "The `is_accessible` is not used by Esmerald Admin, please use `has_permission` instead."
        )

    def has_permission(self, request: Request) -> bool:
        """Override this method to add permission checks.
        Esmerald Admin does not make any assumptions about the authentication system
        used in your application.

        By default, it will allow access for everyone. `has_permission` follows the same pattern
        of Esmerald permission system.
        """
        return True


class BaseView(SQLAdminBaseView, EsmeraldBase):
    ...


class ModelView(SQLAModelView, BaseView):
    ...


class Admin(SQLAdmin):
    """
    Tha base inherited for Saffier which inherits from the base of sqladmin package.
    """

    def __init__(
        self,
        app: Esmerald,
        engine: ENGINE_TYPE,
        base_url: str = "/admin",
        title: str = "Esmerald Administration",
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

    def _find_model_view(self, identity: str) -> ModelView:
        return super()._find_model_view(identity)  # type: ignore

    async def _list(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async def _create(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.can_create or not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async def _details(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.can_view_details or not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async def _delete(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.can_delete or not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async def _edit(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.can_edit or not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    async def _export(self, request: Request) -> None:  # type: ignore
        model_view = self._find_model_view(request.path_params["identity"])  # type: ignore
        if not model_view.can_export or not model_view.has_permission(request):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        if request.path_params["export_type"] not in model_view.export_types:
            raise HTTPException(status_code=404)
