from esmerald import Esmerald

from esmerald_admin import Admin, ModelView

app = Esmerald()
admin = Admin(app, engine)

# Declarative User
DeclarativeUser = User.declarative()


class UserAdmin(ModelView, model=DeclarativeUser):
    column_list = [DeclarativeUser.id, DeclarativeUser.email]


admin.add_view(UserAdmin)
