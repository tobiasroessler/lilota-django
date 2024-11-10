# lilota-django

Light weight solution for long running tasks when using Django.


## Getting Started

In order to install lilota-django in your application yopu have to do the following:

```
pip install lilota-django
```

After that you can integrate it by adding it in the **settings.py**.

```
INSTALLED_APPS = [
  ...
  'lilota_django'
]
```

Now it is time to apply the database changes:

```
python manage.py migrate
```

After the migrations have been applied you will find a new tabel called **lilota_store** in your database. This table contains information about the tasks that are currently running or that already ran.