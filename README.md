# Retry Wrapper

- Adds retries to your functions with the optional email on failure. 
- Useful for scheduled jobs or very long scripts.
___

## Before using
*You must add your own email login info to the credentials.py file formatted as such<br /> 
**Currently only support gmail as the email client, hasn't been tested with other providers

```python
gmail_login = {
    'email':{YOUR EMAIL},
    # gmail app password guide https://support.google.com/accounts/answer/185833?hl=en
    'password':{YOUR EMAIL PASSWORD} 
}
```
## Must include these files for the wrapper to work
```
+-- retry_wrapper
|   +-- __init__.py
|   +-- retry.py
|   +-- credentials.py
```
    
    
## Example of use
```python
from retry_wrapper import *

from random import randint
import credentials # your own credientials file; example above ^

# setup for alert email on failure
email_to = credentials.gmail_login['email']
subject = 'It was not 4'
body = 'Your script did not return the value 4 after 2 attempts'
email_from = credentials.gmail_login['email']

# retry with failure email
@retry(max_retries=2, sec_delay_btwn_retries=2, email_on_fail=email_to, email_subject=subject,
       email_body=body, email_from=email_from)
def is_it_four_email():
    """Does the random number generated equal 4?"""
    x = randint(0, 6)
    assert x == 4, 'This doesn\'t equal 4!!'
    return x

# retry without failure email
@retry(max_retries=2, sec_delay_btwn_retries=2)
def is_it_four_no_email():
    """Does the random number generated equal 4?"""
    x = randint(0, 6)
    assert x == 4, 'This doesn\'t equal 4!!'
    return x
    
is_it_four_no_email()

is_it_four_email()
```
