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
