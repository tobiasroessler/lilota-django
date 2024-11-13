# lilota-django

Light weight solution for long running tasks when using Django. A detailed description about lilota can be found [here](https://github.com/tobiasroessler/lilota).


## Installation

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

After the migrations have been applied you will find a new table called **lilota_store** in your database. This table contains information about the tasks that are currently running or that already ran.


## Usage

### Implement the task you want to execute

First we create a class where we implement our task logic. This class must derive from **TaskBase** and
must contain a **run** method.

Example:
```
from lilota.models import TaskBase

...

class LongRunningTask(TaskBase):

  def run(self):
    self.logger.info("Wait 10 seconds to simulate a long running task")
    time.sleep(10)

    self.set_output(self.task_info.id, {
      "result": self.task_info.input["number1"] + self.task_info.input["number2"]
    })

    self.logger.info("Task finished")
```

In this example we create the task **LongRunningTask**. In the **run** method we wait 10 seconds and then we calculate the sum of two numbers (**number1** and **number2**). For the moment it is not important to understand where **number1** and **number2** are coming from. We come to that very soon. The result is in the end stored in a dictionary and here the key **result** is used. You are free to use whatever name you want for that key and you can use how many keys and values you want of course.

What you can see is that we also log messages here. **lilota-django** is using the build-in **logging** module and
this is already integrated inside the base class **TaskBase** and can be directly used.


### Create a store

**lilota-django** needs a store where all the information about the running tasks are stored. Several store implementations are of course possible. By default **lilota-django** comes with a store that holds its data inside the memory. In the future we will also create a store that connects to a database and is using Django.

Here is an example for our in-memory store:
```
from lilota.stores import StoreManager
from lilota_django.stores import DjangoTaskStore

...

# Create store
StoreManager.register("Store", DjangoTaskStore)
store_manager = StoreManager()
store_manager.start()
store = store_manager.Store()
```

**StoreManager** derives from the **BaseManager** that comes from the **multiprocessing** module in Python. The reason why this is used is to run the store inside its own process in order to access it from all the started processes. More information about such **Managers** can be found [here](https://docs.python.org/3/library/multiprocessing.html#managers).

After the manager is started we get the store from it (store = store_manager.Store()). With that store we can now create a **TaskRunner** instance.


### Create a TaskRunner instance

The heart of lilota is the **TaskRunner** class. It can be instantiated like this:

```
from lilota.runner import TaskRunner

...

runner = TaskRunner(store)
```

The only mandatory parameter is the **store** object we created before.


### Register tasks and start the task runner

As soon as we have our **TaskRunner** object we can register our tasks we want to execute. This registration process does not mean that we run that task but we just make **lilota-django** aware of our task we want to execute.

```
runner.register("long_running_task", LongRunningTask)
runner.start()
```

Two parameters are needed here:
- **name**: The name of our task. That name is used later to execute a task.
- **class**: Here we just add our class that we created above.

As soon as all tasks are registered we can start the task runner. This also does not mean we start all the registered tasks. It only means we start the task runner and the task runner is waiting for the tasks.


### Lets feed the task runner

Now that we have a running instance of our **TaskRunner**, we want to execute our created task. In order to do that you have to execute the following:

```
runner.add("long_running_task", "This task adds two numbers", {"number1": 1, "number2": 2})
```

Here we add a task to the runner by specifying the name ("long_running_task") that we used before when we registered the task. The second argument is a description we can add. And the third argument is a dictionary with the **input parameters**. Here in this example we pass a dictionary with the two keys **number1** and **number2** and their values. These input parameters can be used then in the task itself. You can put whatever you want in that dictionary.


### Data inside the store

As soon as the task is running information about the task are stored in the store. We can get for example all tasks with the following command:

```
tasks = store.get_all_tasks()
print(f"Result: { tasks[0].output["result"] }")
```

This is a very simplyfied version that would fail when the output is not already set. Remember **lilota-django** is a task runner that executes tasks in different processes and the store is available everywhere. So it is possible that the task is saved in the store but still running. Below we print a complete example where we wait until the task is done.


### Stop lilota

When the application is closed and **lilota-django** is not needed anymore you can stop it and close the store.

```
runner.stop()
store_manager.shutdown()
```

You have to do it in that order. When lilota gets stopped it is waiting for tasks that are still running.


### The complete example:

```
from lilota.runner import TaskRunner
from lilota.models import TaskBase
from lilota.stores import StoreManager
from lilota_django.stores import DjangoTaskStore
import logging
import time


class LongRunningTask(TaskBase):

  def run(self):
    self.logger.info("Start a long running task")
    self.logger.info("Wait 10 seconds to simulate a long running task")
    time.sleep(1)
    self.logger.info("Task finished")

    # Set result
    self.set_output(self.task_info.id, {
      "result": self.task_info.input["number1"] + self.task_info.input["number2"]
    })
    

if __name__ == "__main__":
  # Create store
  StoreManager.register("Store", DjangoTaskStore)
  store_manager = StoreManager()
  store_manager.start()
  store = store_manager.Store()

  # Create task runner
  runner = TaskRunner(store)

  # Register task
  runner.register("long_running_task", LongRunningTask)

  # Start the task runner
  runner.start()

  # Run a task
  runner.add("long_running_task", "This task adds two numbers", {"number1": 1, "number2": 2})

  # Get result from the store (1 + 2 = 3)
  tasks = None
  while True:
    tasks = store.get_all_tasks()
    if tasks[0].progress_percentage >= 100:
      break

  if hasattr(tasks[0], 'output'):
    print(f"Result: { tasks[0].output["result"] }")

  # Stop the task runner
  runner.stop()

  # Close the store because it is running in a separate process
  store_manager.shutdown()
```
