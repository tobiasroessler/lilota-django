import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

import django
django.setup()

from unittest import TestCase, main
from multiprocessing import cpu_count
from lilota.runner import TaskRunner
from lilota.models import TaskBase
from lilota.stores import StoreManager
from .stores import DjangoTaskStore
import logging


class AdditionTask(TaskBase):
  
  def run(self):
    output = {
      "result": self.task_info.input["number1"] + self.task_info.input["number2"]
    }
    self.set_output(self.task_info.id, output)


class ExceptionTask(TaskBase):

  def run(self):
    raise Exception("Boom")
  

class DjangoTaskRunnerTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    pass


  def setUp(self):
    pass


  def test_register___nothing_is_registered___should_not_have_any_registration(self):
    # Arrange & Act
    store, store_manager, runner = self.create_task_runner(1)

    # Assert
    self.assertEqual(len(runner._registrations), 0)


  def create_task_runner(self, number_of_processes: int = cpu_count()):
    StoreManager.register("Store", DjangoTaskStore)
    store_manager = StoreManager()
    store_manager.start()
    store = store_manager.Store()
    runner = TaskRunner(store, number_of_processes, logging_level=logging.INFO)
    return (store, store_manager, runner)
  
if __name__ == '__main__':
  main()