import base64
from pathlib import Path
from json import load as json_load, dump as json_dump
from time import sleep
import requests
from requests.exceptions import RequestException

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

# configuration of the config
SC_FILE = Path("server.config.json")
SERVER_CONFIG = {
    'URL': 'https://psu-server.duckdns.org'
}

if SC_FILE.exists():
    # load server config
    SERVER_CONFIG = json_load(open(SC_FILE, 'r'))
else:
    # create server config and initialize it
    SC_FILE.touch()
    json_dump(SERVER_CONFIG, open(SC_FILE, 'w'))


def save_server_config():
    """
    function to save the current SERVER_CONFIG dict to the corresponding file
    """
    json_dump(SERVER_CONFIG, open(SC_FILE, 'w'))


def make_request(uri, check_status_ok, context=None, session=None):
    """
    function trying to make the request at maximum 5 times
    the 5 attempts are timed in steps
    """
    if context is None:
        context = dict()
    if session is None:
        session = requests.session()

    attempt = 0
    while attempt < 5:
        attempt += 1
        try:
            res = session.post(SERVER_CONFIG['URL'] + uri, context).json()
            # check whether status is ok and redo request if check_status_ok is true
            if check_status_ok and res['status'] != 'ok':
                continue
            return res
        except RequestException as e:
            print("Connection failed. Retry in " + str(attempt * attempt * 4) + "secs.")
            print(e)
            sleep(attempt * attempt * 4)


def generate_rsa_key():
    """
    function creating the needed rsa key
    you have to hand over the new public key to the server
    return: corresponding public key
    """
    # generate RSA-Key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    # store private key in config
    private_key_bytes = private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                  serialization.NoEncryption())
    SERVER_CONFIG['private_key'] = str(private_key_bytes, 'utf-8')
    # store public key in config
    public_key_bytes = private_key.public_key().public_bytes(serialization.Encoding.PEM,
                                                             serialization.PublicFormat.SubjectPublicKeyInfo)
    SERVER_CONFIG['public_key'] = str(public_key_bytes, 'utf-8')
    save_server_config()
    return SERVER_CONFIG['public_key']


def register_at_server():
    """
    function which needs to be called in the setup process to register at server
    and get an identity key which will be stored in the server.config.json file.
    At maximum there will be made 5 attempts to register
    returns: True if the registration was successful, otherwise False
    """

    public_key = generate_rsa_key()
    res = make_request('/psucontrol/register_new_psu', True, {'public_rsa_key': public_key}, None)

    if res['status'] == 'ok':
        SERVER_CONFIG['identity_key'] = res['identity_key']
        SERVER_CONFIG['pairing_key'] = res['pairing_key']
        save_server_config()
        return True
    else:
        return False


def request_challenge(session=None):
    """
    function used to get a challenge for the challenge-response-authentication
    returns the challenge or
    """
    if session is None:
        session = requests.session()

    res = make_request("/psucontrol/get_challenge", True, {'identity_key': SERVER_CONFIG['identity_key']}, session)
    if res['status'] == 'ok':
        return res['challenge']
    else:
        return None


def get_signed_challenge(session=None):
    """
    function used to request a challenge and sign it with the private key
    """
    if session is None:
        session = requests.session()
    # get message
    message = request_challenge(session)
    print(message)

    if message is None:
        # something failed
        return None
    else:
        # sign message with private key
        private_key = serialization.load_pem_private_key(bytes(SERVER_CONFIG['private_key'], 'utf-8'), password=None)
        signed = private_key.sign(bytes(message, 'utf-8'),
                                  padding.PSS(
                                      mgf=padding.MGF1(hashes.SHA256()),
                                      salt_length=padding.PSS.MAX_LENGTH),
                                  hashes.SHA256())
        # return url safe string
        return base64.urlsafe_b64encode(signed)
