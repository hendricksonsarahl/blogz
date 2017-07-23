import hashlib

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hash):
    if make_hash(password) == hash:
        return True

    return False