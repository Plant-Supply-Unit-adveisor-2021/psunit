from pathlib import Path
from json import load as json_load, dump as json_dump
from time import sleep

import requests
from requests.exceptions import RequestException

import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from ui.error import handle_server_error

SERVER_ERROR = {
    '0xC1': {'error_code': '0xC1', 'error_message': 'Could not connect to server'}
}

MAX_ATTEMPTS = 5

# configuration of the config
SC_FILE = Path("server.config.json")
SERVER_CONFIG = {
    'URL': 'http://127.0.0.1:8000'
    # 'URL': 'https://psu-server.duckdns.org'
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


def timeout_after_error(attempt, error, *, multiplier=1):
    """
    function for handing over the error to the ui and handling the timeout
    """
    # check whether there is an attempt left
    if attempt < MAX_ATTEMPTS:
        handle_server_error(error, retry_timeout=attempt ** 3 * multiplier)
        # wait before retry
        sleep(attempt ** 3 * multiplier)
    else:
        handle_server_error(error)


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
    function which needs to be called in the setup process to register at server in order
    to get an identity and pairing key which will be stored in the server.config.json file.
    At maximum there will be made 5 attempts to register
    returns: True if the registration was successful, otherwise False
    """

    session = requests.session()
    attempt = 0

    while attempt < MAX_ATTEMPTS:

        attempt += 1

        # generate rsa keys
        public_key = generate_rsa_key()

        # try to make the request
        try:
            res = session.post(SERVER_CONFIG['URL'] + '/psucontrol/register_new_psu',
                               data={'public_rsa_key': public_key}).json()
        except RequestException:
            timeout_after_error(attempt, SERVER_ERROR['0xC1'], multiplier=10)
            continue

        # check response for errors
        if res['status'] == 'ok':
            SERVER_CONFIG['identity_key'] = res['identity_key']
            SERVER_CONFIG['pairing_key'] = res['pairing_key']
            save_server_config()
            return True

        elif res['status'] == 'failed' and res['error_code'] == '0xD1':
            timeout_after_error(attempt, res)

        else:
            # some other wired error -> do not retry
            handle_server_error(res)
            return False

    return False


def request_challenge(session=None):
    """
    function used to get a challenge for the challenge-response-authentication
    returns the challenge or None
    """
    if session is None:
        session = requests.session()

    attempt = 0

    while attempt < MAX_ATTEMPTS:

        attempt += 1

        # try to make the request
        try:
            res = session.post(SERVER_CONFIG['URL'] + '/psucontrol/get_challenge',
                               data={'identity_key': SERVER_CONFIG['identity_key']}).json()
        except RequestException:
            timeout_after_error(attempt, SERVER_ERROR['0xC1'], multiplier=10)
            continue

        # check response for errors
        if res['status'] == 'ok':
            return res['challenge']
        else:
            # some wired error -> do not retry
            handle_server_error(res)
            return None

    return None


def get_signed_challenge(session=None):
    """
    function used to request a challenge and sign it with the private key
    """
    if session is None:
        session = requests.session()

    # get message
    message = request_challenge(session)

    if message is None:
        # something failed
        return None

    # sign message with private key
    private_key = serialization.load_pem_private_key(bytes(SERVER_CONFIG['private_key'], 'utf-8'), password=None)
    signed = private_key.sign(bytes(message, 'utf-8'),
                              padding.PSS(
                                  mgf=padding.MGF1(hashes.SHA256()),
                                  salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
    # return url safe string
    return base64.urlsafe_b64encode(signed)


def post_data(temperature, air_humidity, ground_humidity, brightness, fill_level, timestamp_str):
    """
    function used to submit data to the server
    """
    session = requests.session()

    context = dict()
    context['signed_challenge'] = get_signed_challenge(session)
    context['identity_key'] = SERVER_CONFIG['identity_key']
    # add measurements to the context
    context['temperature'] = temperature
    context['air_humidity'] = air_humidity
    context['ground_humidity'] = ground_humidity
    context['brightness'] = brightness
    context['fill_level'] = fill_level
    context['timestamp'] = timestamp_str

    print(context['signed_challenge'])

    return make_request('/psucontrol/add_data_measurement', True, context, session)
