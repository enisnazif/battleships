from man.battleships.exceptions import MaxRetriesExceededException
from man.battleships.config import MAX_RETRIES


def retry(exceptions, max_retries=MAX_RETRIES):
    """
    Retry decorator that retries the wrapped function a maximum of 'max_retries' times if 'exception' is raised

    :param exceptions: Tuple
    :param max_retries:
    :return:
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            n_retries = 0
            while n_retries < max_retries:
                try:
                    return f(*args, **kwargs)
                except exceptions:
                    n_retries += 1
                    continue
            raise MaxRetriesExceededException

        return f_retry

    return deco_retry
