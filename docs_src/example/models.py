from esmerald.conf import settings
from esmerald.contrib.auth.saffier.base_user import AbstractUser

database, models = settings.db_access


class User(AbstractUser):
    """Inherits from the user base"""

    class Meta:
        registry = models

    def __str__(self):
        return f"{self.email}"
