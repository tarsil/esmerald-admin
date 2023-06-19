# Esmerald Admin

<p align="center">
  <a href="https://esmerald-admin.tarsild.io"><img src="https://res.cloudinary.com/dymmond/image/upload/v1673619342/esmerald/img/logo-gr_z1ot8o.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>The needed admin for Saffier ORM with Esmerald.</em>
</p>

<p align="center">
<a href="https://github.com/tarsil/esmerald_admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/tarsil/esmerald_admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
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

## Esmerald admin for [Saffier][saffier] ORM

Esmerald admin is a flexible user interface for [Saffier ORM][saffier] built on the top of the
already existing and highly maintained [SQLAdmin][sqladmin].

The main goal, as the name of the package says, is to provide a nice, flexible and easy to use
user interface that interacts with [Saffier ORM][saffier] in a more friendly manner.

## Saffier

[Saffier][saffier] is a flexible and powerfull ORM built on the top of SQLAlchemy core that allows
you to interact with almost every single SQL database out there in an asynchronous mode.

### Documentation

Majority of the documentation for this package **can and should** be seen in the [SQLAdmin][sqladmin]
official documentation (don't forget to leave a star on that repository) as the core remains exactly
the same.

The custom, unique, Esmerald way is placed here within these docs.

**Main features include:**

* SQLAlchemy sync/async engines
* Esmerald integration
* [Saffier][saffier] support
* Modern UI using Tabler

## Installation

```shell
$ pip install esmerald-admin
```

## Quickstart

Saffier is a very powerfull ORM as mentioned before and built on the top of SQLAlchemy core but
also extremely flexible allowing to use the models in a `declarative` way, which is the way
SQLAdmin is expecting to use.

This makes Saffier unique since you can use the declarative models for the admin and the core
models for anything else.

See the [declarative models][saffier_declarative] for more details on this.

Let us create a some Saffier models first. This example assumes you use the [contrib user][https://esmerald.dev/databases/saffier/models/]
from Esmerald.

!!! Warning
    Using the user provided by Esmerald is **not mandatory** and you can use your own design.
    The documentation uses the one provided by Esmerald as it is easier to explain and use.

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

    ...


# Create the tables
await registry.create_all()
```

**Now using with Esmerald**

Saffier, as mentioned before, has the [declarative models][saffier_declarative] ready to be used.
These models are **only used for the admin**.

```python
from esmerald import Esmerald
from esmerald_admin import Admin, ModelView

app = Esmerald()
admin = Admin(app, engine)

# Declarative User
DeclarativeUser = User.declarative()


class UserAdmin(ModelView, model=DeclarativeUser):
    column_list = [DeclarativeUser.id, DeclarativeUser.email]


admin.add_view(UserAdmin)
```

Or if you want some more "organised".

**Settings**

```python
from functools import cached_property
from typing import Optional

from esmerald.conf.enums import EnvironmentType
from esmerald.conf.global_settings import EsmeraldAPISettings
from saffier import Database, Registry


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

**Models**

```python
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
```

**Admin**

```python
from accounts.models import User as UserModel
from esmerald_admin import Admin, ModelView

# Declarative Models
User = UserModel.declarative()


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.first_name, User.last_name]


def get_views(admin: Admin) -> None:
    """Generates the admin views"""
    admin.add_model_view(UserAdmin)
```

**Application**

```python
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
```

Now visiting `/admin/` (with slash at the end) on your browser you can see the Esmerald admin interface.

## Important

As mentioned before, Esmerald admin is built on the top of [SQLAdmin][esmerald_admin]. Besides some
unique features for Esmerald with Saffier that are documented here, **everything else should be checked**
**in the [SQLAdmin][sqladmin] official documentation** as it works exactly the same.

Massive thanks to [@aminalaee](https://github.com/aminalaee) to get this working so well and without his work, this would not be possible! ⭐️ Star his repo! ⭐️

[esmerald_admin]: https://esmerald-admin.tarsild.io
[esmerald_repo]: https://github.com/tarsil/esmerald-admin
[saffier]: https://saffier.tarsild.io
[sqladmin]: https://aminalaee.dev/sqladmin/
[saffier_declarative]: https://saffier.tarsild.io/models/#declarative-models
