class TimeoutException(Exception):
    """Class to add a timeout attribute to an exception. If an exception is
    raised specifically due to a rate-limits being exceeded, this class can
    be used to add a timeout, indicated how long a task or application should
    wait until retrying.

    Attributes:
         exception (Exception): Base exception raised by any class.
         timeout (int): Number of seconds the task should wait until retrying.
    """

    def __init__(self, exception, timeout):
        self.exception = exception
        self.timeout = timeout

    def __str__(self):
        return str(self.exception)
