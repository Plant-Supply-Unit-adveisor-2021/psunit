import server.interface
from time import sleep


def test():
    #print(server.interface.register_at_server())
    print(server.interface.post_data(23, 50, 100, 99, 20, '2021-03-27_12-03-04'))
