import socket
from server import Server

my_server = Server('127.0.0.1', 8000, 5, socket.AF_INET, socket.SOCK_STREAM)
my_server.run()
