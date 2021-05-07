import os

from settings import UI_LOG_DIR
from datetime import datetime


def add_log_entry(logmsg):
    """
    function to add a new log entry
    """
    ts = datetime.now()
    ulf = os.path.join(UI_LOG_DIR, ts.strftime("%Y-%m-%d_ui.log"))
    
    if not os.path.exists(UI_LOG_DIR):
        os.makedirs(UI_LOG_DIR)
    
    if not os.path.exists(ulf):
        os.mknod(ulf)
    
    file = open(ulf, 'a')
    file.write(logmsg)
    file.close()


def handle_server_error(error_response, *, retry_timeout=0):
    """
    function to handle an occurring server error
    """

    # try translating message
    try:
        error_message_locale = error_response['error_message_'+ui.LANGUAGE]
    except KeyError:
        error_message_locale = error_response['error_message']
    print("SERVER ERROR")
    print('   ERROR_CODE: ' + error_response['error_code'])
    print('   ERROR MESSAGE: ' + error_response['error_message'])
    if retry_timeout != 0:
        print('   TIME TO RETRY: ' + str(retry_timeout))
