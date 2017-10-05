"""This module implements all socket functions."""
import socket
RECV_BUFFER_SIZE = 1024
import json


def connect_to(ip, port, message, ttl=None):
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
        data = json.loads(data)
        return data
    except:
        return None


def get_metrics(ip,port,ip_end,url,array,index):
    try:
        message = {"action":"get_metrics","ip":ip_end,"url":url}
        message_str = json.dumps(message)
        array[index] = connect_to(ip, port, message_str, 40)
        return True
    except:
        return False


def get_peers(ip,port):
    try:
        message = {"action":"get_peers"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        return None

def insert_peer(ip,port,my_ip,my_port):
    try:
        message = {"action":"insert_peer","ip":my_ip,"port":my_port}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        print "insert_peer error"


def remove_peer(ip,port,my_ip,my_port):
    try:
        message = {"action":"remove_peer","ip":my_ip,"port":my_port}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        print "remove_peer error"
