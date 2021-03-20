from server.interface import request_challenge, get_signed_challenge, post_data
from time import sleep


def test():
    print(post_data(24.5, 34, 100, 50, 100, "2021-03-20_16-32-08"))
