import random
import string
import time

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


current_time_milli = lambda : int(round(time.time() * 1000))