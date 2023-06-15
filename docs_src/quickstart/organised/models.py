import saffier
from esmerald.conf import settings
from esmerald.contrib.auth.saffier.base_user import AbstractUser

database, models = settings.db_access


class BaseModel(saffier.Model):
    class Meta:
        abstract = True
        registry = models


class User(BaseModel, AbstractUser):
    """Inherits from the user base"""

    ...
