# Esmerald Admin

<p align="center">
  <a href="https://esmerald-admin.tarsild.io"><img src="https://res.cloudinary.com/dymmond/image/upload/v1673619342/esmerald/img/logo-gr_z1ot8o.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>The needed admin for Saffier and Edgy with Esmerald.</em>
</p>

<p align="center">
<a href="https://github.com/tarsil/esmerald-admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/tarsil/esmerald-admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald_admin" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald_admin?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald_admin" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald_admin.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://esmerald-admin.tarsild.io][esmerald_admin] 📚

**Source Code**: [https://github.com/tarsil/esmerald-admin][esmerald_repo]

---

## Esmerald admin for [Saffier][saffier] and [Edgy][edgy]

Esmerald admin is a flexible user interface for [Saffier ORM][saffier] and [Edgy][edgy]
built on the top of the already existing and highly maintained [SQLAdmin][sqladmin].

The main goal, as the name of the package says, is to provide a nice, flexible and easy to use
user interface that interacts with [Saffier][saffier] and [Edgy][edgy] in a more friendly manner.

## Saffier

[Saffier][saffier] is a flexible and powerfull ORM built on the top of SQLAlchemy core that allows
you to interact with almost every single SQL database out there in an asynchronous mode.

## Edgy

[Edgy][saffier] is also an extremely, flexible and powerful ORM built on the top of SQLAlchemy core
and **100% Pydantic** with more flexibility for every single use case, also in asynchronous mode.

### Documentation

Majority of the documentation for this package **can and should** be seen in the [SQLAdmin][sqladmin]
official documentation (don't forget to leave a star on that repository) as the core remains exactly
the same.

The custom, unique, Esmerald way is placed here within these docs.

**Main features include:**

* SQLAlchemy sync/async engines
* Esmerald integration
* [Saffier][saffier] support
* [Edgy][edgy] support
* Modern UI using Tabler

## Installation

**For Saffier**

```shell
$ pip install esmerald-admin[saffier]
```

**For Edgy**

```shell
$ pip install esmerald-admin[edgy]
```

**For both**

```shell
$ pip install esmerald-admin[all]
```

## Quickstart

Saffier and Edgy are very powerfull ORMs as mentioned before and built on the top of SQLAlchemy core but
also extremely flexible allowing to use the models in a `declarative` way, which is the way
SQLAdmin is expecting to use.

This makes both Saffier and Edgy unique since you can use the declarative models for the admin and the core
models for anything else.

See the [Saffier declarative models][saffier_declarative] and [Edgy declarative models][edgy_declarative] for more details.

Let us create a some models first. This example assumes you use the [contrib user of Saffier](https://esmerald.dev/databases/saffier/models/)
and the [contrib user of Edgy](https://esmerald.dev/databases/edgy/models/)
from Esmerald.

!!! Warning
    Using the user provided by Esmerald is **not mandatory** and you can use your own design.
    The documentation uses the one provided by Esmerald as it is easier to explain and use.

**Saffier**

```python
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


# Create the tables
await registry.create_all()

```

**Edgy**

```python
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

```

**Now using with Esmerald**

Saffier, as mentioned before, has the [declarative models][saffier_declarative] ready to be used.
These models are **only used for the admin**.


```python
from accounts.models import User
from esmerald import Esmerald, settings

from esmerald_admin import Admin, ModelView

database, registry = settings.db_access

app = Esmerald()
admin = Admin(app, registry.engine)

# Declarative User
DeclarativeUser = User.declarative()


class UserAdmin(ModelView, model=DeclarativeUser):
    column_list = [DeclarativeUser.id, DeclarativeUser.email]


admin.add_view(UserAdmin)
```


Or if you want some more "organised".

**Settings**

```python title="myproject/configs/settings.py"
from functools import cached_property
from typing import Optional

from esmerald.conf.enums import EnvironmentType
from esmerald.conf.global_settings import EsmeraldAPISettings
from saffier import Database, Registry # or from edgy import Database, Registry


class AppSettings(EsmeraldAPISettings):
    app_name: str = "My application in production mode."
    title: str = "My app"
    environment: Optional[str] = EnvironmentType.PRODUCTION
    secret_key: str = "esmerald-insecure-key"

    @cached_property
    def db_access(self):
        database = Database("sqlite:///db.sqlite")
        registry = Registry(database=database)
        return database, registry

```

**Saffier Models**

```python title="myproject/apps/accounts/models.py"
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
```

**Edgy Models**

```python title="myproject/apps/accounts/models.py"
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
```

**Admin**

```python title="myproject/admin.py"
from accounts.models import User as UserModel

from esmerald_admin import Admin, ModelView

# Declarative Models
User = UserModel.declarative()


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.first_name, User.last_name]


def get_views(admin: Admin) -> None:
    """Generates the admin views and it is used in
    the `main.py` file.
    """
    admin.add_model_view(UserAdmin)

```

**Application**

```python title="myproject/app.py"
from accounts.models import User
from esmerald import Esmerald, settings

from esmerald_admin import Admin, ModelView

database, registry = settings.db_access

app = Esmerald()
admin = Admin(app, registry.engine)

# Declarative User
DeclarativeUser = User.declarative()


class UserAdmin(ModelView, model=DeclarativeUser):
    column_list = [DeclarativeUser.id, DeclarativeUser.email]


admin.add_view(UserAdmin)
```

Now visiting `/admin/` (with slash at the end) on your browser you can see the Esmerald admin interface.

## Important

As mentioned before, Esmerald admin is built on the top of [SQLAdmin][esmerald_admin]. Besides some
unique features for Esmerald with Saffier that are documented here, **everything else should be checked**
**in the [SQLAdmin][sqladmin] official documentation** as it works exactly the same.

Massive thanks to [@aminalaee](https://github.com/aminalaee) to get this working so well and without his work, this
would not be possible! ⭐️ Star his repo! ⭐️


[esmerald_admin]: https://esmerald-admin.tarsild.io
[esmerald_repo]: https://github.com/tarsil/esmerald-admin
[saffier]: https://saffier.tarsild.io
[edgy]: https://edgy.tarsild.io
[sqladmin]: https://aminalaee.dev/sqladmin/
[saffier_declarative]: https://saffier.tarsild.io/models/#declarative-models
[edgy_declarative]: https://edgy.tarsild.io/models/#declarative-models
