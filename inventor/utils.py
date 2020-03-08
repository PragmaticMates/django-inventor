import hashlib
import random
from datetime import datetime


def generate_hash(length=16):
    random_number = str(random.random())
    current_data = str(datetime.now())
    salt = hashlib.sha1(random_number.encode('utf-8')).hexdigest()
    pepper = hashlib.sha1(current_data.encode('utf-8')).hexdigest()
    digest = hashlib.sha1((salt + pepper).encode('utf-8')).hexdigest()
    return digest[:length]
