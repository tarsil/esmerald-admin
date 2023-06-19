import os
import sys
from pathlib import Path

from esmerald import Esmerald, Include, settings
from saffier import Migrate, Registry

from esmerald_admin import Admin
from esmerald_admin.backends.email import EmailAdminAuth


def build_path():
    """
    Builds the path of the project and project root.
    """
    Path(__file__).resolve().parent.parent
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    if SITE_ROOT not in sys.path:
        sys.path.append(SITE_ROOT)
        sys.path.append(os.path.join(SITE_ROOT, "apps"))


def get_migrations(app: Esmerald, registry: Registry) -> None:
    """
    Manages the saffier migrations
    """
    Migrate(app, registry)


def get_admin(app, registry):
    """Starts the Esmerald admin"""
    from accounts.models import User

    from .admin import get_views

    auth_backend = EmailAdminAuth(
        secret_key=settings.secret_key,
        auth_model=User,
        config=settings.jwt_config,
    )
    admin = Admin(app, registry.engine, authentication_backend=auth_backend)

    # Get the views
    get_views(admin)


def get_application():
    """
    This is optional. The function is only used for organisation purposes.
    """
    build_path()

    database, registry = settings.db_access

    app = Esmerald(
        routes=[Include(namespace="myproject.urls")],
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
    )

    # Migrations
    get_migrations(app, registry)

    # Admin
    get_admin(app, registry)

    return app


app = get_application()
