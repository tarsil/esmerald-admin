from typing import AsyncGenerator

import edgy
import pytest
from anyio import from_thread, sleep, to_thread
from edgy.testclient import DatabaseTestClient as Database
from esmerald import Esmerald, EsmeraldAPISettings, Request
from esmerald.config.jwt import JWTConfig
from esmerald.contrib.auth.edgy.base_user import AbstractUser
from httpx import AsyncClient
from tests.settings import DATABASE_URL

from esmerald_admin import Admin, ModelView

pytestmark = pytest.mark.anyio

database = Database(DATABASE_URL)
models = edgy.Registry(database=database)


def blocking_function():
    from_thread.run(sleep, 1)


class TestSettings(EsmeraldAPISettings):
    @property
    def jwt_config(self) -> JWTConfig:
        """
        A JWT object configuration to be passed to the application middleware
        """
        return JWTConfig(signing_key=self.secret_key, auth_header_types=["Bearer", "Token"])


class User(AbstractUser):
    ...

    class Meta:
        tablename = "users"
        registry = models


class Address(edgy.Model):
    street: str = edgy.CharField(max_length=255)
    zip_code: str = edgy.CharField(max_length=10)

    class Meta:
        registry = models


@pytest.fixture(autouse=True, scope="function")
async def create_test_database():
    await models.create_all()
    yield
    await models.drop_all()


@pytest.fixture(autouse=True)
async def rollback_transactions():
    with database.force_rollback():
        async with database:
            yield


UserDeclarative = User.declarative()
AddressDeclarative = Address.declarative()


class UserAdmin(ModelView, model=UserDeclarative):
    column_list = [UserDeclarative.id, UserDeclarative.email]


class AddressAdmin(ModelView, model=AddressDeclarative):
    name_plural = "Addresses"
    column_list = [AddressDeclarative.street, AddressDeclarative.zip_code]

    def has_permission(self, request: Request) -> bool:
        return False


settings = TestSettings()

app = Esmerald(
    settings_config=settings, on_startup=[database.connect], on_shutdown=[database.disconnect]
)
admin = Admin(app=app, engine=models.engine)

admin.add_view(UserAdmin)
admin.add_view(AddressAdmin)


@pytest.fixture()
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        await to_thread.run_sync(blocking_function)
        yield ac


async def test_root_view(client: AsyncClient) -> None:
    response = await client.get("/admin/")

    assert response.status_code == 200
    assert '<span class="nav-link-title">Users</span>' in response.text
    assert '<span class="nav-link-title">Addresses</span>' in response.text


async def test_invalid_page(client: AsyncClient) -> None:
    response = await client.get("/admin/test/list")

    assert response.status_code == 404


async def test_has_permission_method(client: AsyncClient) -> None:
    response = await client.get("/admin/address/list")

    assert response.status_code == 403
