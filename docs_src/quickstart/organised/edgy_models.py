import edgy
from esmerald.conf import settings
from esmerald.contrib.auth.edgy.base_user import AbstractUser

database, models = settings.db_access


class BaseModel(edgy.Model):
    class Meta:
        abstract = True
        registry = models


class User(BaseModel, AbstractUser):
    """Inherits from the user base"""

    ...
