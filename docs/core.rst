:mod:`core` --- worker threads
==============================

.. py:currentmodule:: src.worker_threads.core


All classes inherit from the conventional `Thread <https://docs.python.org/3/library/threading.
html#thread-objects>`_ class and the new :ref:`ThreadControlMixin <link-thread-control-mixin>`
class.

CycleWorker
-----------
To make use of this class simply subclass the :class:`CycleWorkerThread` class and overwrite the
:meth:`~CycleWorkerThread.run_routine`. No other methods (except for the constructor) should be
overridden in a subclass. From this point on everything works like a conventional thread objects.

.. code-block:: python

   from worker_threads import CycleWorkerThread


   class MyCycleWorker(CycleWorkerThread):
       def __init__(self):
           super().__init__()

       def run_routine(self):
           pass  # Put your code here


There is another way to specify the activity by passing a callable object to the constructor.

.. code-block:: python

   from worker_threads import CycleWorkerThread


   def run_routine():
       pass  # Put your code here


   worker = CycleWorkerThread(target=run_routine)


.. class:: CycleWorkerThread(delay=0.0, timeout=1000.0, target=None, args=(), kwargs={}, daemon=None)

    This class represents a special thread type, which executes a predefined routine
    cyclically until a stop event is triggered.

   .. py:attribute:: delay

      Indicates how much time shall pass before the worker continues with
      the next cycle.

   .. py:attribute:: timeout

      Indicates how much time the worker is allowed to pause before the
      worker is automatically forced to stop.

   .. method:: run()

      Defines the worker's concrete workflow.

   .. method:: run_routine()

      Representing the worker's activity on each cycle.

      You may override this method in a subclass. The run_routine() method
      invokes the callable object passed to the object's constructor as the
      target argument, if any, with sequential and keyword arguments taken
      from the args and kwargs arguments, respectively.

   .. method:: is_working()

      Returns ``True`` if the worker is running a routine, ``False`` otherwise.

   .. method:: preparation()

      Optional preparatory steps for the worker to perform before starting.

   .. method:: post_processing()

      Optional follow-up steps for the worker to perform after stoppage.

TaskWorker
----------
To make use of this class simply subclass the :class:`TaskWorkerThread` class and overwrite the
:meth:`~CycleWorkerThread.run_task`. No other methods (except for the constructor) should be
overridden in a subclass. From this point on everything works like a conventional thread objects.

.. code-block:: python

   from worker_threads import TaskWorkerThread


   class MyTaskWorker(TaskWorkerThread):
       def __init__(self, tasks):
           super().__init__(tasks)

       def run_task(self, task):
           pass  # Put your code here


.. class:: TaskWorkerThread(tasks, delay=0.0, timeout=1000.0, daemon=None)

    This class represents a special thread type, which processes a stack of
    similar tasks one after the other.

   .. py:attribute:: delay

      Indicates how much time shall pass before the worker continues with
      the next task.

   .. py:attribute:: timeout

      Indicates how much time the worker is allowed to pause before the
      worker is automatically forced to stop.

   .. method:: run()

      Defines the worker's concrete workflow.

   .. method:: run_task(task)

      Abstract method representing the worker's activity on all task.

   .. method:: is_working()

      Returns ``True`` if the worker is running a task, ``False`` otherwise.

   .. method:: preparation()

      Optional preparatory steps for the worker to perform before starting.

   .. method:: post_processing()

      Optional follow-up steps for the worker to perform after stoppage.
