"""This module implements all socket functions."""
import socket
RECV_BUFFER_SIZE = 1024


def connect_to(ip, port, message, reply, ttl=None):
    """Connect to node (ip, port)."""
    data = ''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ttl is not None:
            sock.settimeout(ttl)
        server_address = (ip, int(port))
        sock.connect(server_address)
        sock.sendall(str(message))
        data = sock.recv(RECV_BUFFER_SIZE)
        sock.close()
        if(data == reply):
            return True
        else:
            raise Exception('Not the appropriate reply')
    except:
        return False
