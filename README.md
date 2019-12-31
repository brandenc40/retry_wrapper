# Retry Wrapper

Adds retries to your functions

```python
@retry(num_retries=1, delay_seconds=3, log_exception=True)
def test_func():
    return 8/0

test_func(fake_arg=124)

> WARNING:root:{'failed_function': 'test_func', 'exception': ZeroDivisionError('division by zero',), 
> 'attempt_number': 1, 'args': (), 'kwargs': {'fake_arg': 124}}
> 
> ZeroDivisionError                         Traceback (most recent call last)
> <ipython-input-27-d640b419f916> in <module>()
>       3     return 8/0
>       4 
> --->  5 test_func()
> 
> <ipython-input-26-fe691ff26d5e> in run_in_loop(*args, **kwargs)
>      29                 except Exception as e:
>      30                     if retry_attempt == num_retries:
> ---> 31                         raise e
>      32                     if log_exception:
>      33                         logging.warning('{}() failed with exception: {}'.format(func.func_name, e))
> 
> ZeroDivisionError: integer division or modulo by zero
```
