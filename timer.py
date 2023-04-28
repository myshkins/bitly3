import time


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """start a new timer"""
        self._start_time = time.perf_counter()

    def stop(self):
        """stop the timer, and print elapsed time"""
        execution_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Executed in : {execution_time} sec")
