# Notes

Some threading practice, all code is working

To gain some understanding on locks, thread pools, blocking. 

```python3
import random
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

SENTINEL = object()

## this is the intermediary, kind of like a queue.
class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer. Only one messages is processed at a time though here in this implementation. The processor processes a message and then runs into a lock.

    While it works for this limited test, it is not a great solution to the producer-consumer problem in general because it only allows a single value in the pipeline at a time. When the producer gets a burst of messages, it will have nowhere to put them.
    """
#     def __init__(self):
#         self.message = 0
#         self.producer_lock = threading.Lock()
#         self.consumer_lock = threading.Lock()
#         self.consumer_lock.acquire()
#
#     def get_message(self, name):
#         logging.debug("%s:about to acquire getlock", name)
#         self.consumer_lock.acquire()
#         logging.debug("%s:have getlock", name)
#         message = self.message
#         logging.debug("%s:about to release setlock", name)
#         self.producer_lock.release()
#         logging.debug("%s:setlock released", name)
#         return message
#
#     def set_message(self, message, name):
#         logging.debug("%s:about to acquire setlock", name)
#         self.producer_lock.acquire()
#         logging.debug("%s:have setlock", name)
#         self.message = message
#         logging.debug("%s:about to release getlock", name)
#         self.consumer_lock.release()
#         logging.debug("%s:getlock released", name)
#
#
# def producer(pipeline):
#     """Pretend we're getting a message from the network."""
#     for index in range(4):
#         message = random.randint(1, 10)
#         logging.info("Producer got message: %s", message)
#         pipeline.set_message(message, "Producer")
#
#     # Send a sentinel message to tell consumer we're done
#     pipeline.set_message(SENTINEL, "Producer")
#
#
# def consumer(pipeline):
#     """Pretend we're saving a number in the database."""
#     message = 0
#     while message is not SENTINEL:
#         message = pipeline.get_message("Consumer")
#         if message is not SENTINEL:
#             logging.info("Consumer storing message: %s", message)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
#
#     logging.getLogger().setLevel(logging.DEBUG)
#
#     pipeline = Pipeline()
#
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline)
#         executor.submit(consumer, pipeline)
#
#


# =============== using a queue
import queue
import concurrent.futures
import time


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)

def consumer(pipeline, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(
            "Consumer storing message: %s  (queue size=%s)",
            message,
            pipeline.qsize(),
        )

    logging.info("Consumer received EXIT event. Exiting")

def producer(pipeline, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    logging.info("Producer received EXIT event. Exiting")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.03)
        logging.info("Main: about to set event")
        event.set()






# ========== final code
# import concurrent.futures
# import logging
# import queue
# import random
# import threading
# import time
#
# def producer(queue, event):
#     """Pretend we're getting a number from the network."""
#     while not event.is_set():
#         message = random.randint(1, 101)
#         logging.info("Producer got message: %s", message)
#         queue.put(message)
#
#     logging.info("Producer received event. Exiting")
#
# def consumer(queue, event):
#     """Pretend we're saving a number in the database."""
#     while not event.is_set() or not queue.empty():
#         message = queue.get()
#         logging.info(
#             "Consumer storing message: %s (size=%d)", message, queue.qsize()
#         )
#
#     logging.info("Consumer received event. Exiting")
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     pipeline = queue.Queue(maxsize=10)
#     event = threading.Event()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline, event)
#         executor.submit(consumer, pipeline, event)
#
#         time.sleep(0.1)
#         logging.info("Main: about to set event")
#         event.set()
✔ ~/Desktop/programming/interview_questions/threading [master|✚ 11…4]
13:13 $ cat practice.py
# from concurrent.futures import ThreadPoolExecutor
# from queue import Queue
#
#
# q = Queue()
#
#
# def producer(thread_id):
#     print('thread_id: ', thread_id)
#     return thread_id
#
#
# def consumer():
#     return None
#
#
# def divide_and_conquer():
#     thread_count = 4
#
#     with ThreadPoolExecutor(max_workers=thread_count) as executor:
#         futures = [executor.submit(producer, i) for i in range(thread_count)]
#         for future in futures:
#             print('future: ', future.result())
#
#
# if __name__ == '__main__':
#     divide_and_conquer()


"""
The order in which threads are run is determined by the operating system and can be quite hard to predict. It may (and likely will) vary from run to run, so you need to be aware of that when you design algorithms that use threading.

Fortunately, Python gives you several primitives that you’ll look at later to help coordinate threads and get them running together. Before that, let’s look at how to make managing a group of threads a bit easier.
"""
#
#
#
# import logging
# import threading
# import time
#
# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(3)
#     logging.info("Thread %s: finishing", name)
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
#
#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()
#
#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)

# from concurrent.futures import ThreadPoolExecutor
# import logging
# import time


# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#
#     def update(self, name):
#         logging.info("Thread %s: starting update", name)
#         local_copy = self.value
#         local_copy += 1
#         time.sleep(0.1)
#         self.value = local_copy
#         logging.info("Thread %s: finishing update", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.update, index)
#     logging.info("Testing update. Ending value is %d.", database.value)


# ================== with lock
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)
    logging.info("Testing update. Ending value is %d.", database.value)
```
