from typing import AsyncGenerator, Generator

import pytest
import saffier
from anyio import from_thread, sleep, to_thread
from esmerald import Esmerald, EsmeraldAPISettings
from esmerald.config.jwt import JWTConfig
from esmerald.contrib.auth.saffier.base_user import AbstractUser
from esmerald.testclient import EsmeraldTestClient
from httpx import AsyncClient
from saffier.testclient import DatabaseTestClient as Database
from tests.settings import DATABASE_URL

from esmerald_admin import Admin
from esmerald_admin.backends import EmailAdminAuth, UsernameAdminAuth

pytestmark = pytest.mark.anyio

database = Database(DATABASE_URL)
models = saffier.Registry(database=database)


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


settings = TestSettings()


def get_email_backend_admin() -> Admin:
    app = Esmerald(
        settings_config=settings, on_startup=[database.connect], on_shutdown=[database.disconnect]
    )

    email_authentication_backend = EmailAdminAuth(
        secret_key=settings.secret_key, auth_model=User, config=settings.jwt_config
    )
    admin = Admin(
        app=app, engine=models.engine, authentication_backend=email_authentication_backend
    )
    return app, admin


def get_username_backend_admin() -> Admin:
    app = Esmerald(
        settings_config=settings, on_startup=[database.connect], on_shutdown=[database.disconnect]
    )

    user_authentication_backend = UsernameAdminAuth(
        secret_key=settings.secret_key, auth_model=User, config=settings.jwt_config
    )
    admin = Admin(
        app=app, engine=models.engine, authentication_backend=user_authentication_backend
    )
    return app, admin


@pytest.fixture
def email_client() -> Generator[EsmeraldTestClient, None, None]:
    app, _ = get_email_backend_admin()

    with EsmeraldTestClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture
def username_client() -> Generator[EsmeraldTestClient, None, None]:
    app, _ = get_username_backend_admin()

    with EsmeraldTestClient(app=app, base_url="http://testserver") as c:
        yield c


@pytest.fixture()
async def async_client_email() -> AsyncGenerator:
    app, _ = get_email_backend_admin()
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        await to_thread.run_sync(blocking_function)
        yield ac


@pytest.fixture()
async def async_client_username() -> AsyncGenerator:
    app, _ = get_username_backend_admin()
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        await to_thread.run_sync(blocking_function)
        yield ac


async def get_user(password="test"):
    return await User.query.create_user(
        username="test",
        password=password,
        email="foo@bar.com",
        first_name="foo",
        last_name="bar",
        is_superuser=False,
        is_staff=True,
    )


def test_access_login_required_views_with_email_backend_auth(
    email_client: EsmeraldTestClient,
) -> None:
    response = email_client.get("/admin/")
    assert response.url == "http://testserver/admin/login"

    response = email_client.get("/admin/users/list")
    assert response.url == "http://testserver/admin/login"


def test_access_login_required_views_with_username_backend_auth(
    username_client: EsmeraldTestClient,
) -> None:
    response = username_client.get("/admin/")
    assert response.url == "http://testserver/admin/login"

    response = username_client.get("/admin/users/list")
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_with_email_backend(async_client_email: AsyncClient) -> None:
    response = await async_client_email.post(
        "/admin/login", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_with_username_backend(async_client_email: AsyncClient) -> None:
    response = await async_client_email.post(
        "/admin/login", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_no_superuser_with_email_backend(
    async_client_email: AsyncClient,
) -> None:
    user = await get_user()

    response = await async_client_email.post(
        "/admin/login", data={"username": user.email, "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_no_superuser_with_username_backend(
    async_client_username: AsyncClient,
) -> None:
    user = await get_user()

    response = await async_client_username.post(
        "/admin/login", data={"username": user.username, "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_no_staff_with_email_backend(
    async_client_email: AsyncClient,
) -> None:
    user = await get_user()
    await user.update(
        is_superuser=True,
        is_staff=False,
    )

    response = await async_client_email.post(
        "/admin/login", data={"username": user.email, "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def test_login_failure_no_staff_with_username_backend(
    async_client_username: AsyncClient,
) -> None:
    user = await get_user()
    await user.update(
        is_superuser=True,
        is_staff=False,
    )

    response = await async_client_username.post(
        "/admin/login", data={"username": user.username, "password": "test"}
    )

    assert response.status_code == 400
    assert response.url == "http://testserver/admin/login"


async def xtest_login_with_email_backend(
    async_client_email: AsyncClient,
) -> None:
    user = await get_user()
    await user.update(
        is_superuser=True,
        is_staff=True,
    )

    response = await async_client_email.post(
        "/admin/login", data={"username": user.email, "password": "test"}
    )

    assert len(response.cookies) == 1


async def test_login_with_username_backend(
    async_client_username: AsyncClient,
) -> None:
    user = await get_user()
    await user.update(
        is_superuser=True,
        is_staff=True,
    )

    response = await async_client_username.post(
        "/admin/login", data={"username": user.username, "password": "test"}
    )

    assert len(response.cookies) == 1


async def test_logout(
    async_client_username: AsyncClient,
) -> None:
    response = await async_client_username.get("/admin/logout")

    assert len(response.cookies) == 0
