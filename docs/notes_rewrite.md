# Notes

On may 9th and 10th, I rewrote the ingestor.

I read on the Python docs that this was a better way to ingest the data:

```python3
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
# import threading
# import logging
# import time
# from concurrent.futures import ThreadPoolExecutor
#
#
# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()
#
#     def locked_update(self, name):
#         logging.info("Thread %s: starting update", name)
#         logging.debug("Thread %s about to lock", name)
#         with self._lock:
#             logging.debug("Thread %s has lock", name)
#             local_copy = self.value
#             local_copy += 1
#             time.sleep(0.1)
#             self.value = local_copy
#             logging.debug("Thread %s about to release lock", name)
#         logging.debug("Thread %s after release", name)
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
#             executor.submit(database.locked_update, index)
#     logging.info("Testing update. Ending value is %d.", database.value)



# probably do this for your takehome
# import logging
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     # logging.getLogger().setLevel(logging.DEBUG)
#
#     pipeline = Pipeline()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline)
#         executor.submit(consumer, pipeline)
```

I modeled my rewrite after this code above. Using a queue to sit in between the producer (consumes api and writes to queue) and consumer. Also, I decided to give smaller chunks to the thread while iterating up to the end block which gives more evenly distributed work to each thread. This better utilizes the thread pool. My first approach divided the entire block window into too large chunks to the threads, resulting in some threads living much longer than others... which was inefficient usage of the thread pool. This uneven distribution of transactions was a result of the sort of... an F distribution of transactions throughout the block range (i.e, the earlier part of the block range simply had more transactions so giving it entirely to 1 thread to process was inefficient.)

With the additional consumer, we don't fall too far behind the queue:

```python3
2024-05-10 12:14:50,664 - INFO - thread_id: Consumer_thread_0. Message: About to save... 5000 records.
2024-05-10 12:14:50,760 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12414682&endblock=12423182&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 178
2024-05-10 12:14:50,843 - INFO - thread_id: Consumer_thread_0. Message: Batch saved. Current transaction queue size: 185756. Current db size: 115000
2024-05-10 12:14:50,863 - INFO - thread_id: 1. Message: Calling Etherscan API with current_block: 12414682, ending_block: 12423182, thread_id: 1
2024-05-10 12:14:50,866 - DEBUG - Starting new HTTPS connection (1): api.etherscan.io:443
2024-05-10 12:14:50,901 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12736682&endblock=12745182&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-10 12:14:50,932 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12856682&endblock=12872682&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 None
2024-05-10 12:14:51,013 - INFO - thread_id: Consumer_thread_1. Message: About to save... 5000 records.
2024-05-10 12:14:51,104 - DEBUG - https://api.etherscan.io:443 "GET /api?module=account&action=txlistinternal&address=0xE592427A0AEce92De3Edee1F18E0157C05861564&startblock=12414682&endblock=12423182&page=1&offset=10000&sort=asc&apikey=H4PV22WR9MSNYJM25TN9FFXEZGB3NFDX6V HTTP/1.1" 200 178
2024-05-10 12:14:51,189 - INFO - thread_id: Consumer_thread_1. Message: Batch saved. Current transaction queue size: 185363. Current db size: 120000
```
