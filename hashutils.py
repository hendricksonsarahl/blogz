import hashlib
import random
import string

# Makes a random string of letters 5 letters in length
def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


# Hash user's password, salt it and store both the pw and the salt

def make_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password)).hexdigest()
    return '{0},{1}'.format(hash, salt)


# verify entered password against previously hashed/salted password in db
def check_hash(password, hash):
    salt = hash.split(',')[1]
    if make_hash(password, salt) == hash:
        return True
    else:
        return False