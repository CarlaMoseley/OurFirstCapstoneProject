#SHA256 method for passwords
import hashlib

def hash_password(password):
    hash_password = hashlib.sha256(password.enconde('utf-8'))
    return hash_password.hexdigest()