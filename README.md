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




WEITER HIER





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

When using self.client.post inside view tests then you also have to add the following in the settings.py file:

```
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
```

Without it the status code in the response is a 400.



# Asynchronous tasks (using RabbitMQ)


## Docker

* Install **Ranger Desktop**
* Login to Docker by opening the terminal and enter:
```
docker login
``` 
(use the username and password stored in KeePassXC)


## RabbitMQ

* Pull **rabbitmq** in Ranger Desktop
* Start RabbitMQ on the terminal:
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```
* Open the browser and enter the following URL: **http://localhost:15672/**. On the page you have to login (use **guest** as username and password).


## Celery

* Install Celery
```
pip install celery
```
* Add Celery to your project. Create a new file **celery.py** in the main app folder where the **settings.py** can also be found.
* Add the following:
```
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```
* Edit the app/__init__.py file and add the following code to it:
```
# Import celery
from .celery import app as celery_app
__all__ = ['celery_app']
```
* Running a Celery worker
```
celery -A app worker -l info
```


## Monitoring Celery with Flower

* Install Flower
```
pip install flower
```
* Create **flowerconfig.py** file in the **app** application and add the following:
```
# RabbitMQ management api
broker = 'http://guest:guest@localhost:5672/'
broker_api = 'http://guest:guest@localhost:15672/api/'

# Enable debug logging
logging = 'INFO'
```
This is optional but I think it makes sence to mention it here. Even when only changing the logging level.
* Launch Flower
```
celery -A app flower --conf=app/flowerconfig.py
```
**--conf=app/flowerconfig.py** is only needed when we add the file.