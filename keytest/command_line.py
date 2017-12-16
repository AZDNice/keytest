
import os.path
import sys
import argparse
import keytest

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_der_private_key

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.dh import DHPrivateKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey

from cryptography.hazmat.backends import default_backend

def try_decode(data):
    key = None

    try:
        key = load_pem_private_key(
            data=data,
            password=None,
            backend=default_backend())
    except ValueError:
        pass
    else:
        return key
    
    return key

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('keyfile', metavar='FILE',
                        help='file containing an asymmetric private key')

    parser.add_argument('--mr-trials', metavar='TRIALS',
                        type=int, default=32,
                        help='number of Miller Rabin trials (default: 32)')

    args = parser.parse_args()

    if not os.path.isfile(args.keyfile):
        message='no such key file: {}'.format(args.keyfile)
        parser.error(message)

    data = None

    with open(args.keyfile, 'rb') as io:
        data = io.read()

    key = try_decode(data)

    if key == None:
        message='unrecognized key format: {}'.format(args.keyfile)
        parser.error(message)

    if isinstance(key, RSAPrivateKey):
        keytest.test_rsa(key, args.mr_trials)

    
