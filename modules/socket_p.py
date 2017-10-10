"""This module implements all socket functions."""
import socket
RECV_BUFFER_SIZE = 1024
import json
from files_db import add_file_f

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


def get_metrics(ip,port,no_of_pings,url,array,index):
    try:
        message = {"action":"get_metrics","url":url,"no_of_pings":no_of_pings}
        message_str = json.dumps(message)
        array[index] = connect_to(ip, port, message_str, 45)
        return True
    except:
        array[index] = None
        return False


def get_peers(ip,port):
    try:
        message = {"action":"get_peers"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        return None


def get_trackers(ip,port):
    try:
        message = {"action":"get_trackers"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        return None


def get_local_files(ip,port):
    try:
        message = {"action":"get_local_files"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 20)
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


def get_all_files(ip,port):
    try:
        message = {"action":"get_all_files"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 50)
    except:
        return None




def download_via(ip,port,url):
    data=''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, int(port))
        sock.connect(server_address)
        message = {"action":"download_via","url":url}
        message_str = json.dumps(message)
        name=url.split('/')[-1]
        t1=time.time()
        sock.sendall(str(message))
        while(True):
            data=data+sock.recv(1024)
            if "<EOF>" in data:
                break
        sock.close()
        lines=data.split('\n')
        f=open("Downloads/"+name,"wb+")
        for i in range(0,len(lines)-1):
            f.write(lines[i]+"\n")
        f.close()
        t2=time.time()
        print "Download time:",float("{0:.2f}".format((t2-t1)*100)),"ms"
        add_file_f(name,url,via=False)
        return True
    except:
        return False


def download_directly(url,via=False):
    try:
        temp=url.split('/')
        name=temp[-1]
        t1=time.time()
        file=urllib.urlretrieve(url,name)[0]
        t2=time.time()
        print "Download time:",float("{0:.2f}".format((t2-t1)*100)),"ms"
        if via:
            os.rename(file,"Cache/"+file)
        else:
            os.rename(file,"Downloads/"+file)
        add_file_f(name,url,via=via)
        return True
    except:
        return False