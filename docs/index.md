# Esmerald Admin

<p align="center">
  <a href="https://esmerald-admin.tarsild.io"><img src="https://res.cloudinary.com/dymmond/image/upload/v1673619342/esmerald/img/logo-gr_z1ot8o.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>The needed admin for Saffier ORM with Esmerald.</em>
</p>

<p align="center">
<a href="https://github.com/tarsil/esmerald_admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/tarsil/esmerald_admin/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald_admin" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald_admin?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald_admin" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald_admin.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://esmerald-admin.tarsild.io][esmerald_admin] 📚

**Source Code**: [https://github.com/tarsil/esmerald-admin][esmerald_repo]

---

## Esmerald admin for [Saffier][saffier] ORM

Esmerald admin is a flexible user interface for [Saffier ORM][saffier] built on the top of the
already existing and highly maintained [SQLAdmin][sqladmin].

The main goal, as the name of the package says, is to provide a nice, flexible and easy to use
user interface that interacts with [Saffier ORM][saffier] in a more friendly manner.

## Saffier

[Saffier][saffier] is a flexible and powerfull ORM built on the top of SQLAlchemy core that allows
you to interact with almost every single SQL database out there in an asynchronous mode.

### Documentation

Majority of the documentation for this package **can and should** be seen in the [SQLAdmin][sqladmin]
official documentation (don't forget to leave a star on that repository) as the core remains exactly
the same.

The custom, unique, Esmerald way is placed here within these docs.

**Main features include:**

* SQLAlchemy sync/async engines
* Esmerald integration
* [Saffier][saffier] support
* Modern UI using Tabler

## Installation

```shell
$ pip install esmerald-admin
```

## Quickstart

Saffier is a very powerfull ORM as mentioned before and built on the top of SQLAlchemy core but
also extremely flexible allowing to use the models in a `declarative` way, which is the way
SQLAdmin is expecting to use.

This makes Saffier unique since you can use the declarative models for the admin and the core
models for anything else.

See the [declarative models][saffier_declarative] for more details on this.


[esmerald_admin]: https://esmerald-admin.tarsild.io
[esmerald_repo]: https://github.com/tarsil/esmerald-admin
[saffier]: https://saffier.tarsild.io
[sqladmin]: https://aminalaee.dev/sqladmin/
[saffier_declarative]: https://saffier.tarsild.io/models/#declarative-models
