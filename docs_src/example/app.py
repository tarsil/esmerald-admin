import os
import sys
from pathlib import Path

from esmerald import Esmerald, Include, settings
from saffier import Migrate, Registry


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

    return app


app = get_application()
