import datetime
import time


LOGGING_LEVEL_NOTHING = 0
LOGGING_LEVEL_CONSOLE = 1
LOGGING_LEVEL_FILE = 2
LOGGING_LEVEL_ALL = 3


class Timer:

    _DEFAULT_ACCURACY = 8

    def __init__(self, name=None, file_name=None, logging_level=None,
                 accuracy=None):
        self.name = name
        self.file_name = file_name
        self.logging_level = logging_level
        if accuracy:
            self.accuracy = accuracy
        else:
            self.accuracy = self._DEFAULT_ACCURACY

        self.result = None

    def __enter__(self):
        self.time_start = time.time()

    def __exit__(self, type_, value, traceback):
        self.result = time.time() - self.time_start
        message = f"Elapsed: {self.result:.{self.accuracy}f} seconds"
        if self.name:
            message = f"[{self.name}] -> {message}."

        if self._check_logging_level(LOGGING_LEVEL_CONSOLE):
            print(message)

        if self.file_name and self._check_logging_level(LOGGING_LEVEL_FILE):
            with open(self.file_name, "a") as file_out:
                print(f"{datetime.datetime.now()} :", message, file=file_out)

    def _check_logging_level(self, logging_level_to_check):
        return self.logging_level & logging_level_to_check


class RepeatedTimer(Timer):

    def __init__(self, name=None, file_name=None, logging_level=None,
                 accuracy=None):
        super().__init__(name=name, file_name=file_name,
                         logging_level=logging_level, accuracy=accuracy)
        self.total_result = None
        self.average_result = None

    def run(self, test_args, n_times):
        self.total_result = 0
        for _ in range(n_times):
            with self:
                for subject, args in test_args.items():
                    if args:
                        if isinstance(args, tuple):
                            for arg in args:
                                subject(arg)
                        else:
                            subject(*args)
                    else:
                        subject()
            self.total_result += self.result

        self.average_result = self.total_result / n_times

        message = f"Elapsed:\t\t" \
                  f"total result={self.total_result:.{self.accuracy}f} " \
                  f"seconds;\t\t" \
                  f"average result={self.average_result:.{self.accuracy}f} " \
                  f"seconds."
        if self.name:
            message = f"[{self.name}] -> {message}"

        if self._check_logging_level(LOGGING_LEVEL_CONSOLE):
            print(message)
        if self.file_name and self._check_logging_level(LOGGING_LEVEL_FILE):
            with open(self.file_name, "a") as file_out:
                print(f"{datetime.datetime.now()} :", message, end="\n\n",
                      file=file_out)
