import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import sys

KEY = b"it-is-a-secret-hidden-unk9wn-key"  # this is unkhown by the attacker and 32 bytes long
BS = AES.block_size  # AES block size

from flask import Flask
from flask import request

app = Flask(__name__)


class UnpadException(Exception):
    pass

def _get_blocks(c):
    return [c[i * BS : i * BS + BS] for i in range(len(c) // BS)]

def _unpad(s):
    padlen = s[-1]
    for i in s[-padlen:]:
        if padlen != i:
            raise UnpadException
    return s[:-padlen]

def _pad(s):
    if len(s) % BS == 0:
        padded = s + bytes([BS]) * BS
    else:
        padded = s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
    return padded

@app.route("/encrypt")
def encrypt():
    r = {}
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, IV=iv)
    r["ciphertext"] = (iv + cipher.encrypt(_pad(b"this is a secre|t message that |no one should k|now.->pad"))).hex()
    return json.dumps(r)


@app.route("/process")
def process():
    ciphertext = bytes.fromhex(request.args.get('cipher'))
    blocks = _get_blocks(ciphertext)
    iv = blocks[0]
    cipher = AES.new(KEY, AES.MODE_CBC, IV=iv)
    paddedtext = cipher.decrypt(b"".join(blocks[1:]))
    plaintext = ""
    try:
        plaintext = _unpad(paddedtext)
        print(plaintext)
        return json.dumps({}), 200
    except unpadException:
        return json.dumps({}), 500


if __name__ == "__main__":
    app.run()
