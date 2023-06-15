import saffier
from esmerald.contrib.auth.saffier.base_user import AbstractUser
from saffier import Database, Registry

database = Database("sqlite:///db.sqlite")
registry = Registry(database=database)


class BaseModel(saffier.Model):
    class Meta:
        abstract = True
        registry = registry


class User(BaseModel, AbstractUser):
    """Inherits from the user base"""

    ...


# Create the tables
await registry.create_all()
