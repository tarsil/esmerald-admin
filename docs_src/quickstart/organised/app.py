import os
import sys
from pathlib import Path

from esmerald import Esmerald, Include, settings

from esmerald_admin import Admin


def build_path():
    """
    Builds the path of the project and project root.
    """
    Path(__file__).resolve().parent.parent
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    if SITE_ROOT not in sys.path:
        sys.path.append(SITE_ROOT)
        sys.path.append(os.path.join(SITE_ROOT, "apps"))


def get_admin(app, registry):
    """Starts the saffier admin"""
    from .admin import get_views

    admin = Admin(app, registry.engine)

    # Get the views function from the "admin.py"
    get_views(admin)


def get_application():
    """
    This is optional. The function is only used for organisation purposes.
    """
    build_path()

    # Registry that comes from the "settings.py"
    # This is Saffier related and centralised in the settings
    # file, as per Esmerald design
    database, registry = settings.db_access

    app = Esmerald(
        routes=[Include(namespace="linezap.urls")],
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
    )

    # Admin
    get_admin(app, registry)

    return app


app = get_application()
