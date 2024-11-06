# lilota-django
Light weight solution for long running tasks when using Django


## Development

### Setup the project

**Create a virtual environment with venv**

This is needed in order to have an insolated area so different versions of packages do not interfer with eachother.

```
python3 -m venv ~/.virtualenvs/lilota-django
```

**Activate the virtual environment**

```
source ~/.virtualenvs/lilota-django/bin/activate
```

**Use Python from the virtual environment**

In VSCode: View -> Command Palette... -> Python: Select Interpreter -> Enter the following path:
```
/Users/torox/.virtualenvs/lilota-django/bin/python
```

**Upgrade pip**

```
python3 -m pip install --upgrade pip
```

**Install from a requirements.txt file**

```
pip install -r requirements.txt
```

### Run server

```
python3 manage.py runserver
```



# Database

## Create initial migrations

```
python3 manage.py makemigrations
```

## Apply the migrations

```
python3 manage.py migrate
```

## Remove all migrations

```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

After that drop the database and execute again:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Create super user

```
python3 manage.py createsuperuser
```



# Account lilotadjango

```
python3 manage.py startapp lilotadjango
```



# Unit tests

If you want for example create tests for an app (like the person app) then just create a directory called tests inside the person app. In that directory place a file called __init__.py. **This is important to tell python that the directory is a package.**

After that create a file to test the models. The file is called test_models.py.

When the tests are created you can open a terminal an enter the following in the root directory of your application:

```
(pyapp) macbook-tobi:pyapp torox$ ./manage.py test person --settings=app.settings_for_tests
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```

When running a test in the sidebar then the following needs to be added at the beginning of each test:

```
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
django.setup()
```
