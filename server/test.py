from server.interface import request_challenge, get_signed_challenge, post_data


def test():
    print(post_data(24.5, 34, 100, 50, 100))
