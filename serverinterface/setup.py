from pathlib import Path
import json
import requests

SC_FILE = Path("server.config.json")

# standard start configuration
SERVER_CONFIG = {
    'URL': 'https://psu-server.duckdns.org'
}

if not SC_FILE.exists():
    # create server config and initialize it
    SC_FILE.touch()
    json.dump(SERVER_CONFIG, open(SC_FILE, 'w'))
else:
    # load server config
    SERVER_CONFIG = json.load(open(SC_FILE, 'r'))


def register_at_server():
    """
    function which needs to be called in the setup process to register at server
    and get an identity key which will be stored in the server.config.json file.
    """
    r = requests.post(SERVER_CONFIG['URL'] + '/psucontrol/register_new_psu')
    data = r.json()
    if data['status'] == 'ok':
        SERVER_CONFIG['identity_key'] = data['identity_key']
        json.dump(SERVER_CONFIG, open(SC_FILE, 'w'))
