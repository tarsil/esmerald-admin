from datetime import datetime

from edgy.exceptions import ObjectNotFound
from esmerald import Request

from esmerald_admin.backends.saffier.base import BaseAuthentication

DEFAULT_HEADER = "Bearer"


class UsernameAdminAuth(BaseAuthentication):
    """
    Uses the AuthenticationProtocol from esmerald_admin assuming it is using the
    Esmerald contrib user and login into the admin.
    """

    async def login(self, request: Request) -> bool:  # type: ignore
        form = await request.form()
        username, password = form["username"], form["password"]

        try:
            user = await self.auth_model.query.get(username=username)
        except ObjectNotFound:
            return False

        is_password_valid = await user.check_password(password)
        if (
            is_password_valid
            and self.is_user_able_to_authenticate(user)
            and self.is_user_staff_and_superuser(user)
        ):
            time = datetime.now() + self.config.access_token_lifetime
            token = self.generate_user_token(user, time=time)
            request.session.update({"token": token})
            return True

        return False
