from pathlib import Path
import os
from json import load as json_load, dump as json_dump
from json.decoder import JSONDecodeError

from time import sleep
from datetime import datetime, timedelta

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
    'last_push': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
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
        except (RequestException, JSONDecodeError):
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
        except (RequestException, JSONDecodeError):
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


def post_data(temperature, air_humidity, ground_humidity, brightness, fill_level, timestamp_str, *, session=None):
    """
    function used to submit data to the server
    returns: success of operation
    """
    if session is None:
        session = requests.session()

    context = dict()

    # add identification information
    context['identity_key'] = SERVER_CONFIG['identity_key']

    # add measurements to the context
    context['temperature'] = temperature
    context['air_humidity'] = air_humidity
    context['ground_humidity'] = ground_humidity
    context['brightness'] = brightness
    context['fill_level'] = fill_level
    context['timestamp'] = timestamp_str

    attempt = 0

    while attempt < MAX_ATTEMPTS:

        attempt += 1

        # get authentication information
        context['signed_challenge'] = get_signed_challenge(session)
        if context['signed_challenge'] is None:
            # something with getting the challenge went wrong
            return False

        # try to make the request
        try:
            res = session.post(SERVER_CONFIG['URL'] + '/psucontrol/add_data_measurement',
                               data=context).json()
        except (RequestException, JSONDecodeError):
            timeout_after_error(attempt, SERVER_ERROR['0xC1'], multiplier=10)
            continue

        # check response for errors
        if res['status'] == 'ok' or (res['status'] == 'failed' and res['error_code'] == '0xD4'):
            # ok or measurement already exists
            return True

        elif res['status'] == 'failed' and (res['error_code'] == '0xD2' or res['error_code'] == '0xA2'):
            # database or authentication error -> retry
            timeout_after_error(attempt, res)

        else:
            # some other wired error -> do not retry
            handle_server_error(res)
            return False

    return False


def push_data():
    """
    function to go through the logs an send recent data to the server
    """
    current = last = datetime.strptime(SERVER_CONFIG['last_push'], '%Y-%m-%d_%H-%M-%S')

    session = requests.session()

    while datetime.now().date() - current.date() >= timedelta():

        try:
            file = open('data/' + current.strftime('%Y-%m-%d') + '.log', 'r')
        except FileNotFoundError:
            # no data exists -> skip
            current += timedelta(days=1)
            continue

        # iterate through entries
        for line in file.readlines():
            data = line.split(';')

            if len(data) != 6:
                # non valid data
                continue
            if datetime.strptime(data[0], '%Y-%m-%d_%H-%M-%S') - last <= timedelta():
                # data already pushed
                continue

            if post_data(data[1], data[2], data[3], data[4], data[5], data[0], session=session):
                # worked out fine -> set last push to this timestamp
                SERVER_CONFIG['last_push'] = data[0]
            else:
                # something wrong -> try later
                save_server_config()
                file.close()
                return False

        # close file and set current to the next day
        file.close()
        current += timedelta(days=1)

    save_server_config()
    return True


def enter_data(temperature, air_humidity, ground_humidity, brightness, fill_level, *, timestamp=datetime.now()):
    """
    function used to enter the measured data
    the data will be stored in the data directory to keep it stored locally for backup purposes
    additionally these files will be used to post the data
    """

    # create data directory
    os.makedirs('data', exist_ok=True)

    # write data entry
    file = open('data/' + timestamp.strftime('%Y-%m-%d') + '.log', 'a')
    file.write(timestamp.strftime('%Y-%m-%d_%H-%M-%S') + ';' +
               str(temperature) + ';' + str(air_humidity) + ';' + str(ground_humidity) + ';' +
               str(brightness) + ';' + str(fill_level) + '\n')
    file.close()


def post_image(image, *, session=None):
    """
    function to post an image to the server
    image needs to be an file object for now
    returns success of operation
    """
    if session is None:
        session = requests.session()

    context = dict()

    # add identification information and timestamp
    context['identity_key'] = SERVER_CONFIG['identity_key']
    context['timestamp'] = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # create dict with file
    files = {'image': open(image, 'rb')}

    attempt = 0

    while attempt < MAX_ATTEMPTS:

        attempt += 1

        # get authentication information
        context['signed_challenge'] = get_signed_challenge(session)
        if context['signed_challenge'] is None:
            # something with getting the challenge went wrong
            return False

        # try to make the request
        try:
            res = session.post(SERVER_CONFIG['URL'] + '/psucontrol/add_image',
                               data=context, files=files).json()
        except (RequestException, JSONDecodeError):
            timeout_after_error(attempt, SERVER_ERROR['0xC1'], multiplier=10)
            continue

        # check response for errors
        if res['status'] == 'ok' or (res['status'] == 'failed' and res['error_code'] == '0xD4'):
            # ok or image already exists
            return True

        elif res['status'] == 'failed' and (res['error_code'] == '0xD2' or res['error_code'] == '0xA2'):
            # database or authentication error -> retry
            timeout_after_error(attempt, res)

        else:
            # some other wired error -> do not retry
            handle_server_error(res)
            return False

    return False
