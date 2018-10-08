import base64
import hashlib


def encode(src):
    return base64.b64encode(src.encode()).decode()


def decode(src):
    return base64.b64decode(src.encode()).decode()


def md5(src):
    return hashlib.md5(src.encode()).hexdigest()


print(md5('zaq1xsw2'))
