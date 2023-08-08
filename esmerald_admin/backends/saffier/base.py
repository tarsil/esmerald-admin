from typing import Any

from esmerald.exceptions import AuthenticationError, NotAuthorized
from saffier.exceptions import DoesNotFound

from esmerald_admin.backends.base import BackendBaseAuthentication

DEFAULT_HEADER = "Bearer"


class BaseAuthentication(BackendBaseAuthentication):
    """
    Uses the AuthenticationProtocol from esmerald_admin assuming it is using the
    Esmerald contrib user and login into the admin.
    """

    async def retrieve_user(self, token_sub: Any) -> Any:
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
