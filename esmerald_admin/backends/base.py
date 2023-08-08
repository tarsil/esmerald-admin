from datetime import datetime, timedelta
from typing import Any, Optional

from esmerald import Request
from esmerald.exceptions import AuthenticationError
from esmerald.security.jwt.token import Token
from jose import JWSError, JWTError
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse

DEFAULT_HEADER = "Bearer"


class BackendBaseAuthentication(AuthenticationBackend):
    """
    Uses the AuthenticationProtocol from esmerald_admin assuming it is using the
    Esmerald contrib user and login into the admin.
    """

    def __init__(self, secret_key: str, auth_model: Any, config: Any) -> None:
        super().__init__(secret_key)
        self.auth_model = auth_model
        self.config = config

    def generate_user_token(self, user: Any, time: Any = None) -> str:
        """
        Generates the JWT token for the authenticated user.
        """
        if not time:
            later = datetime.now() + timedelta(minutes=20)
        else:
            later = time

        token = Token(sub=user.id, exp=later)
        return token.encode(key=self.config.signing_key, algorithm=self.config.algorithm)

    def is_user_able_to_authenticate(self, user: Any) -> bool:
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    def is_user_staff_and_superuser(self, user: Any) -> bool:
        """Checks if a user is staff and superuser to acess the admin"""
        return bool(user.is_staff and user.is_superuser)

    async def clear_session(self, request: Request) -> None:
        """Clears the login sessions form the browser"""
        request.session.clear()

    async def logout(self, request: Request) -> bool:  # type: ignore
        """Logout from the admin"""
        await self.clear_session(request)
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:  # type: ignore
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
            await self.clear_session(request)
            raise AuthenticationError("User not found.")
