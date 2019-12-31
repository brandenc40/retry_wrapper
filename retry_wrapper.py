import logging
import time


def retry(num_retries=2, delay_seconds=0.5, log_exception=False):
    """
    Decorator used to retry after failure

    :arg int num_retries: (Default: 2) How many times the function should be retried
    :arg int delay_seconds: (Default: 0.5) How long to wait between retry attempts
    :arg boolean log_exception: (Default: False) Whether or not exceptions should be logged

    Example:
        @retry(num_retries=1, delay_seconds=3, log_exception=True)
        def test_func():
            return 8/0

        test_func()
    """
    def decorator(func):
        def run_in_loop(*args, **kwargs):
            retry_attempt = 0
            while retry_attempt <= num_retries:
                if delay_seconds and retry_attempt > 0:
                    time.sleep(delay_seconds)
                try:
                    x = func(*args, **kwargs)
                    return x
                except Exception as e:
                    if retry_attempt == num_retries:
                        raise e
                    elif log_exception:
                        logging.warning({
                            "failed_function": func.__name__,
                            "exception": e,
                            "attempt_number": retry_attempt + 1,
                            "args": args,
                            "kwargs": kwargs
                        })
                    retry_attempt += 1
        return run_in_loop
    return decorator
