# time_functions.py

import random
import time

def random_sleep(min, max):
	time.sleep(random.randint(min, max)/10)
