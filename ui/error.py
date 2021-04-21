import ui


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
    print('   ERROR MESSAGE LOCALE: ' + error_message_locale)
    if retry_timeout != 0:
        print('   TIME TO RETRY: ' + str(retry_timeout))
