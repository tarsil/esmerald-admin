from edgy import Database, Registry
from esmerald import Request
from esmerald.contrib.auth.edgy.base_user import AbstractUser

from esmerald_admin import ModelView

database = Database("sqlite:///db.sqlite")
registry = Registry(database=database)


class User(AbstractUser):
    """Inherits from the user base"""

    class Meta:
        registry = registry


# Use the declarative from Saffier
UserDeclarative = User.declarative()


class UserAdmin(ModelView, model=UserDeclarative):
    def is_visible(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticationBackend
        return True

    def has_permission(self, request: Request) -> bool:
        # Check incoming request
        # For example request.session if using AuthenticationBackend
        return True
