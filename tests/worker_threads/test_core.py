import queue
import time
import unittest
from unittest import mock
from src.worker_threads.core import (
    CycleWorkerThread,
    TaskWorkerThread
)


class CycleWorkerThreadClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    CycleWorkerThread class within <src.worker_threads.core>.
    """
    @staticmethod
    def run_routine() -> None:
        """
        Simulating a specific worker, that needs 100 ms to finish it's
        work routine.
        """
        time.sleep(0.1)

    def setUp(self):
        self.__worker = CycleWorkerThread(target=self.run_routine)

    def tearDown(self):
        del self.__worker

    def test_property_delay(self):
        """
        This test checks if the property delay is set correctly.
        """
        self.assertEqual(self.__worker.delay, 0.0)
        self.__worker.delay = 1.0
        self.assertEqual(self.__worker.delay, 1.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.delay = -1.0
        self.assertTrue("Delay must be non-negative" in str(context.exception))

    def test_property_timeout(self):
        """
        This test checks if the property timeout is set correctly.
        """
        self.assertEqual(self.__worker.timeout, 1000.0)
        self.__worker.timeout = 500.0
        self.assertEqual(self.__worker.timeout, 500.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.timeout = -500.0
        self.assertTrue("Timeout must be non-negative" in str(context.exception))

    def test_start_pause_resume_stop(self):
        """
        This test checks if a worker can transition into all states.
        """
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_paused_state()

        self.__worker.resume()
        self._verify_running_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_stop(self):
        """
        This test checks if a worker can be forced to stop working during PAUSED state.
        """
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_paused_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_timeout(self):
        """
        This test checks if a worker automatically stops working once the maximum
        pause time passed.
        """
        self.__worker.timeout = 1.0
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_stopped_state()

    def test_target_None(self):
        """
        This test checks if a worker without a work routine is stopped immediately.
        """
        self.__worker = CycleWorkerThread(target=None)
        self._verify_initial_state()
        self.__worker.start()
        self._verify_stopped_state()

    def _verify_initial_state(self):
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_initial())
        self.assertIn("initial", repr(self.__worker))

    def _verify_running_state(self):
        self.assertTrue(self.__worker.is_alive())
        self.assertTrue(self.__worker.is_running())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("running", repr(self.__worker))

    def _verify_paused_state(self):
        while self.__worker.is_working():
            time.sleep(0.005)
        self.assertTrue(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_paused())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("paused", repr(self.__worker))

    def _verify_stopped_state(self):
        self.__worker.join(timeout=2.0)
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_stopped())
        self.assertIn("stopped", repr(self.__worker))


class TaskWorkerThreadClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    TaskWorkerThread class within <src.worker_threads.core>.
    """
    class SpecificTaskWorker(TaskWorkerThread):
        """
        Simulating a specific worker, that needs 100 ms to finish one task.
        """
        def __init__(self, tasks) -> None:
            super().__init__(tasks)

        def run_task(self, task: int) -> None:
            time.sleep(0.1)

    def setUp(self):
        tasks = queue.Queue()
        for i in range(5000):
            tasks.put(i)
        self.__worker = self.SpecificTaskWorker(tasks)

    def tearDown(self):
        del self.__worker

    def test_property_delay(self):
        """
        This test checks if the property delay is set correctly.
        """
        self.assertEqual(self.__worker.delay, 0.0)
        self.__worker.delay = 1.0
        self.assertEqual(self.__worker.delay, 1.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.delay = -1.0
        self.assertTrue("Delay must be non-negative" in str(context.exception))

    def test_property_timeout(self):
        """
        This test checks if the property timeout is set correctly.
        """
        self.assertEqual(self.__worker.timeout, 1000.0)
        self.__worker.timeout = 500.0
        self.assertEqual(self.__worker.timeout, 500.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.timeout = -500.0
        self.assertTrue("Timeout must be non-negative" in str(context.exception))

    def test_start_pause_resume_stop(self):
        """
        This test checks if a worker can transition into all states.
        """
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_paused_state()

        self.__worker.resume()
        self._verify_running_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_stop(self):
        """
        This test checks if a worker can be forced to stop working during PAUSED state.
        """
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_paused_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_timeout(self):
        """
        This test checks if a worker automatically stops working once the maximum
        pause time passed.
        """
        self.__worker.timeout = 1.0
        self._verify_initial_state()

        self.__worker.start()
        self._verify_running_state()

        self.__worker.pause()
        self._verify_stopped_state()

    def test_worker_end_no_tasks_left(self):
        """
        This test checks if a worker automatically stops working once all tasks
        are done.
        """
        tasks = queue.Queue()
        tasks.put(1)
        self.__worker = self.SpecificTaskWorker(tasks)
        self.__worker.start()
        self._verify_stopped_state()

    def test_worker_end_queue_empty_exception(self):
        """
        This test checks if a worker stops working once an empty queue exception
        was caught.
        """
        tasks = queue.Queue()
        tasks.put(1)
        self.__worker = self.SpecificTaskWorker(tasks)

        m1 = mock.Mock()
        root = "src.worker_threads.core"
        with mock.patch(f"{root}.queue.Queue.get", m1, create=True):
            m1.side_effect = self._mock_queue_get
            self.__worker.start()
            self._verify_stopped_state()

    def _verify_initial_state(self):
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_initial())
        self.assertIn("initial", repr(self.__worker))

    def _verify_running_state(self):
        self.assertTrue(self.__worker.is_alive())
        self.assertTrue(self.__worker.is_running())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("running", repr(self.__worker))

    def _verify_paused_state(self):
        while self.__worker.is_working():
            time.sleep(0.005)
        self.assertTrue(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_paused())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("paused", repr(self.__worker))

    def _verify_stopped_state(self):
        self.__worker.join(timeout=2.0)
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertTrue(self.__worker.is_stopped())
        self.assertIn("stopped", repr(self.__worker))

    def _mock_queue_get(self):
        raise queue.Empty
