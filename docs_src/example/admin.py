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
