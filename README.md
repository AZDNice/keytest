
# `keytest`

Takes an asymmetric keypair and tests it against the NIST FIPS 186-4
requirements in Appendix B. For RSA keys, this does not check whether the
factors or their assocaited primes are correctly generated as probably or
provable primes.

**WARNING**: This is meant as a tool to test the ability of a cryptographic
library to generate correct keys. This is **NOT** for testing production key
strength. I reserve the right sneakily add code that will email me every key you
run through this tool. You have been warned.

## Install

Download this repository and change to the root directory.

Install with `pip3` without administrative privileges:

    pip3 --install --user .
    
Install inside a python virtual environment for development:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip3 --install -e .

Not compatible with Python 2.

## Usage

To demonstrate how this works, generate an RSA key:

    openssl genrsa -out rsa_private.pem 1024

Now, execute the `keytest` command line script:

    keytest ./rsa_private.pem
    
You'll see output like this:

    PASS: e > 2^16
    PASS: e < 2^256
    PASS: e is odd
    PASS: e is coprime with p-1
    PASS: e is coprime with q-1
    PASS: p is probably prime
    PASS: q is probably prime
    PASS: p > sqrt(2) * 2^(nlen/2 - 1)
    PASS: p < 2^(nlen/2) - 1
    PASS: q > sqrt(2) * 2^(nlen/2 - 1)
    PASS: q < 2^(nlen/2) - 1
    PASS: |p-q| > 2^(nlen/2 - 100)
    PASS: d > 2^(nlen/2)
    PASS: d < LCM(p-1,q-1)
    PASS: e*d == 1 mod LCM(p-1,q-1)
    
Each of the statements on the right are requirements of the key. For instance,
the first test requires that the `e` parameter of the RSA key is greater than
`2^16`.

## Changelog

 * 2017-12-16
   - Initial version
   - Supports RSA PEM files only
   

