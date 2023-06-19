# Authentication

Like SQLAdmin, Esmerald Admin does not enfoce any authentication, but provides two out-of-the-box
optional `EmailAdminAuth` and `UsernameAdminAuth` using the [Esmerald contrib auth][models] for
Saffier that you can use.

!!! Note
    If you don't use the Esmerald models for Saffier, you can simply ignore this and use your own
    implementation and follow the instructions from the [SQLAdmin][sqladmin_models].


## EmailAdminAuth and UsernameAdminAuth

These two authentication backends use the `AuthenticationBackend` from [SQLAdmin][sqladmin_models]
and apply logins using `email` or `username`, your choice.

`EmailAdminAuth` and `UsernameAdminAuth` expect three parameters:

* `secret_key` - The secret to be used with your auth.
* `auth_model` - The class object of your `User`, usually derived from the [User model][user_model].
* `config` - The application settings object. It can be the [settings config][settings_config] or
the application `settings` from `esmerald.conf`. It all depends of which one you use.

### How to use

This is how you could use the backends in your Esmerald application. This example is very simple
and it will use the [settings_config][settings_config] from Esmerald to simplify. This is not
mandatory and you can use your preferred way.

```python hl_lines="43-46"
{!> ../docs_src/auth/example.py !}
```

To use the `UsernameAdminAuth` instead:

```python
from esmerald_admin.backends.username import UsernameAdminAuth
```

The `User` model as you can notice, is the one that derived from Esmerald and the reason for this
is because the Esmerald models come with a lot of functionality already built-in such as password
hashing and checks for passwords and therefore, makes it easier to use it.

!!! Tip
    SQLAdmin has clear instructions in case you want to build your own backend authentication
    from the scratch.

## Using OAuth

This implementation can be found in the official [SQLAdmin](https://aminalaee.dev/sqladmin/authentication/#using-oauth)
side.

## Permissions

Esmerald Admin uses the same base as SQLAdmin but adds some extra uniquenesses to it such as the
pattern for the permissions.

In Esmerald, the [permissions][permissions] are extremely powerfull and yet simple to implement.
**Esmerald admin** opted to follow the same pattern.

What is `is_accessible` in [SQLAdmin][sqladmin_models], in Esmerald admin is called `has_permission`.
This way the consistency is maintained and the common systax preserved.

The `ModelView` and the `BaseView` classes in Esmerald Admin also implement two methods you can
override. These methods are used for the control of each Model/View in addition to the
`AuthenticationBackend`.

* `is_visible` - Controls if the Model/View should be displayed in the menu or not.
* `has_permission` - Controls if the Model/View should be accessed.

Like SQLAdmin, both methods implement the same signature and should return a `bool`.

```python hl_lines="43-46"
{!> ../docs_src/auth/permissions.py !}
```

[models]: https://esmerald.dev/databases/saffier/models/
[user_model]: https://esmerald.dev/databases/saffier/models/#user
[sqladmin_models]: https://aminalaee.dev/sqladmin/authentication/
[settings_config]: https://esmerald.dev/application/settings/#the-settings_config
[permissions]: https://esmerald.dymmond.com/permissions/
