import time
import logging
from typing import Callable

logging.basicConfig(filename='./logs/perf.log', level=logging.DEBUG)

# Real simple performance timer decorator
def p_timer(f: Callable):
    def wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        f(*args, **kwargs)
        t_end = time.perf_counter()
        logging.debug(f'{f.__name__} executed in {t_start - t_end:0.4f} seconds')

    return wrapper
