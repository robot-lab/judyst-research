import datetime
import time


class Timer:

    def __init__(self, name=None, file_name=None):
        self.name = name
        self.file_name = file_name

    def __enter__(self):
        self.time_start = time.time()

    def __exit__(self, type_, value, traceback):
        message = f'Elapsed: {(time.time() - self.time_start):.4f} seconds'
        if self.name:
            message = f'[{self.name}] ' + message
        print(message)
        if self.file_name:
            with open(self.file_name, 'a') as file_out:
                print(str(datetime.datetime.now()) + ":", message,
                      file=file_out)
