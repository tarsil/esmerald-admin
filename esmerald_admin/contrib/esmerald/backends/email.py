from datetime import datetime, timedelta
from typing import Any, Optional, Type

from esmerald import Request
from esmerald.exceptions import AuthenticationError, NotAuthorized
from esmerald.middleware.authentication import AuthResult, BaseAuthMiddleware
from esmerald.security.jwt.token import Token
from jose import JWSError, JWTError
from saffier import Model
from saffier.exceptions import DoesNotFound
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse

DEFAULT_HEADER = "Bearer"


class EmailAdminAuth(AuthenticationBackend, BaseAuthMiddleware):
    """
    Uses the AuthenticationProtocol from esmerald_admin assuming it is using the
    Esmerald contrib user and login into the admin.
    """

    def __init__(self, secret_key: str, auth_model: Type["Model"], config: Any) -> None:
        super().__init__(secret_key)
        self.auth_model = auth_model
        self.config = config

    def generate_user_token(self, user: Type["Model"], time=None):
        """
        Generates the JWT token for the authenticated user.
        """
        if not time:
            later = datetime.now() + timedelta(minutes=20)
        else:
            later = time

        token = Token(sub=user.id, exp=later)
        return token.encode(key=self.config.signing_key, algorithm=self.config.algorithm)

    def is_user_able_to_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        try:
            user = await self.auth_model.query.get(email=email)
        except DoesNotFound:
            return False

        is_password_valid = await user.check_password(password)
        if is_password_valid and self.is_user_able_to_authenticate(user):
            time = datetime.now() + self.config.access_token_lifetime
            token = self.generate_user_token(user, time=time)
            request.session.update({"token": token})
            return True

        return False

    async def clear_session(self, request: Request) -> None:
        """Clears the login sessions form the browser"""
        request.session.clear()

    async def logout(self, request: Request) -> bool:
        """Logout from the admin"""
        await self.clear_session(request)
        return True

    async def retrieve_user(self, token_sub: Any) -> Type["Model"]:
        """
        Retrieves a user from the database using the given token id.
        """
        try:
            sub = int(token_sub)
            token_sub = sub
        except (TypeError, ValueError):
            ...

        user_field = {self.config.user_id_field: token_sub}
        try:
            return await self.auth_model.query.get(**user_field)
        except DoesNotFound:
            raise NotAuthorized() from None
        except Exception as e:
            raise AuthenticationError(detail=str(e)) from e

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        """Authenticates the user and adds to the scope of the application"""
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        token = f"{DEFAULT_HEADER} {token}"
        token_partition = token.partition(" ")
        token_type = token_partition[0]
        auth_token = token_partition[-1]

        if not token_type:
            await self.clear_session(request)
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        try:
            token = Token.decode(
                token=auth_token,
                key=self.config.signing_key,
                algorithms=[self.config.algorithm],
            )
        except (JWSError, JWTError):
            await self.clear_session(request)
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await self.retrieve_user(token.sub)
        if not user:
            raise AuthenticationError("User not found.")
        return AuthResult(user=user)
