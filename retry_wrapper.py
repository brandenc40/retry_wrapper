import time
import logging
from random import randint
from functools import wraps
import smtplib
from email.mime.text import MIMEText
import credentials

GMAIL_USER = credentials.gmail_login['email']
GMAIL_PWRD = credentials.gmail_login['password']


def retry(max_retries=2, sec_delay_btwn_retries=1, email_on_fail=None,
          email_subject=None, email_body=None, email_from=None):
    def retry_func(func):
        @wraps(func)
        def run_trys(*args, **kwargs):
            if email_on_fail:
                assert email_subject, 'Must include an email_subject argument'
                assert email_body, 'Must include an email_body argument'
                assert email_from, 'Must include an email_from argument'
                sec_delay = sec_delay_btwn_retries
                for i in range(1, max_retries+1):
                    try:
                        x = func(*args, **kwargs)
                        return x
                        break
                    except Exception as e:
                        logging.warning(
                            'function failed, retrying.. Exception: {}'.format(e))
                        time.sleep(sec_delay)
                        continue
                msg = MIMEText(str(email_body))
                msg['Subject'] = email_subject
                msg['From'] = email_from
                msg['To'] = email_on_fail
                server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(GMAIL_USER, GMAIL_PWRD)
                server.sendmail(email_from, [email_on_fail], msg.as_string())
                server.close()
                logging.warning('Failed after {} retries. Email sent to {}'.format(
                    max_retries, email_on_fail))
            else:
                sec_delay = sec_delay_btwn_retries
                for i in range(1, max_retries+1):
                    try:
                        x = func(*args, **kwargs)
                        return x
                    except Exception as e:
                        logging.warning(
                            'function failed, retrying.. Exception: {}'.format(e))
                        time.sleep(sec_delay)
                        continue
                logging.warning('Failed after {} retries.'.format(max_retries))
        return run_trys
    return retry_func
