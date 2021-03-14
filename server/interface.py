from pathlib import Path
from json import load as json_load, dump as json_dump
from time import sleep
from requests import post as requests_post
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
    attempts = 0
    while attempts < 5:
        # generate RSA key pair
        public_key = generate_rsa_key()

        # make request to register PSU at server
        try:
            r = requests_post(SERVER_CONFIG['URL'] + '/psucontrol/register_new_psu', {'public_rsa_key': public_key})
            data = r.json()
        except RequestException:
            data = dict(status='failed')
            print('Connection failed')

        # evaluate request
        if data['status'] == 'ok':
            SERVER_CONFIG['identity_key'] = data['identity_key']
            SERVER_CONFIG['pairing_key'] = data['pairing_key']
            save_server_config()
            return True
        else:
            # retry in 60 seconds
            attempts += 1
            sleep(60)

    return False


def test():
    private_key = serialization.load_pem_private_key(bytes(SERVER_CONFIG['private_key'], 'utf-8'), password=None)
    public_key = serialization.load_pem_public_key(bytes(SERVER_CONFIG['public_key'], 'utf-8'))
    print(len(SERVER_CONFIG['public_key']))
    message = bytes('hey', 'utf-8')
    print(str(message, 'utf-8'))
    encrypted = private_key.sign(message,
                                 padding.PSS(
                                     mgf=padding.MGF1(hashes.SHA256()),
                                     salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())
    print(encrypted)
    try:
        public_key.verify(encrypted, bytes('hey', 'utf-8'),
                          padding.PSS(
                              mgf=padding.MGF1(hashes.SHA256()),
                              salt_length=padding.PSS.MAX_LENGTH),
                          hashes.SHA256())
        print('TRUE')
    except InvalidSignature:
        print('WRONG')
