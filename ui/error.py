def handle_server_error(error_response, *, retry_timeout=0):
    """
    function to handle an occurring server error
    """
    print("SERVER ERROR")
    print('   ERROR_CODE: ' + error_response['error_code'])
    print('   ERROR MESSAGE: ' + error_response['error_message'])
    if retry_timeout != 0:
        print('   TIME TO RETRY: ' + error_response['error_message'])
