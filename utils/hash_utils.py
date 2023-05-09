""" Python Hash Functions """
from uuid import uuid4
import hashlib
import re

def hash_text(text):
    """ Takes a given text string, salts it, and SHA256 Hashes it"""
    return hashlib.sha256(text.encode()).hexdigest()

def verify_is_a_hash(full_hash):
    """ Takes a given hash, and checks it is in the correct format. """
    regex_check = "([a-f]|[0-9]){64}"
    if re.match(regex_check, full_hash):
        return True
    else: 
        return False
