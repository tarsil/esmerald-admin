from datetime import datetime, timedelta
from typing import Optional, Type

from esmerald import Redirect, Request
from esmerald.conf import settings
from esmerald.exceptions import AuthenticationError, NotAuthorized
from esmerald.middleware.authentication import AuthResult, BaseAuthMiddleware
from esmerald.security.jwt.token import Token
from esmerald_admin.contrib.esmerald.backends.protocols import AuthenticationProtocol
from jose import JWSError, JWTError
from saffier import Model
from saffier.exceptions import DoesNotFound
from sqladmin.authentication import AuthenticationBackend


class EmailAdminAuth(AuthenticationProtocol, AuthenticationBackend, BaseAuthMiddleware):
    """
    Uses the AuthenticationProtocol from esmerald_admin assuming it is using the
    Esmerald contrib user and login into the admin.
    """

    def generate_user_token(self, user: Type["Model"], time=None):
        """
        Generates the JWT token for the authenticated user.
        """
        if not time:
            later = datetime.now() + timedelta(minutes=20)
        else:
            later = time

        token = Token(sub=user.id, exp=later)
        return token.encode(
            key=settings.jwt_config.signing_key, algorithm=settings.jwt_config.algorithm
        )

    def is_user_able_to_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], ["password"]

        try:
            user = await self.auth_model.query.get(username=username)
        except DoesNotFound:
            await self.auth_model().set_password(password)

        else:
            is_password_valid = await user.check_password(password)
            if is_password_valid and self.is_user_able_to_authenticate(user):
                time = datetime.now() + settings.jwt_config.access_token_lifetime
                token = self.generate_user_token(user, time=time)

                request.session.update({"token": token})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[Redirect]:
        token = request.session.get("token")

        if not token:
            return Redirect(path=request.url_for("admin:login"))

        token_partition = token.partition(" ")
        token_type = token_partition[0]
        auth_token = token_partition[-1]

        if token_type not in self.config.auth_header_types:
            raise NotAuthorized(detail=f"{token_type} is not an authorized header type")

        try:
            token = Token.decode(
                token=auth_token, key=self.config.signing_key, algorithms=[self.config.algorithm]
            )
        except (JWSError, JWTError) as e:
            raise AuthenticationError(str(e)) from e

        user = await self.retrieve_user(token.sub)
        if not user:
            raise AuthenticationError("User not found.")
        return AuthResult(user=user)
