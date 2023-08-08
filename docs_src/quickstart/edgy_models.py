import edgy
from edgy import Database, Registry
from esmerald.contrib.auth.edgy.base_user import AbstractUser

database = Database("sqlite:///db.sqlite")
registry = Registry(database=database)


class BaseModel(edgy.Model):
    class Meta:
        abstract = True
        registry = registry


class User(BaseModel, AbstractUser):
    """Inherits from the user base"""

    ...


# Create the tables
await registry.create_all()
