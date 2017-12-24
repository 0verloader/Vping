"""This module implements all socket functions."""
import socket
RECV_BUFFER_SIZE = 1024
import json
from files_db import add_file_f
import time

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
        exit()
        return None


def get_metrics(ip,port,no_of_pings,ip_end,url,array,index):
    try:
        message = {"action":"get_metrics","url":url,"no_of_pings":no_of_pings,"ip_end":ip_end}
        message_str = json.dumps(message)
        ret_m = connect_to(ip, port, message_str, 45)
        array[index] = (ret_m['ping'] , ret_m['RTT'])
        return True
    except:
        array[index] = (None,None)
        return False


def get_peers(ip,port):
    try:
        message = {"action":"get_peers"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        return None

def connect_to_tlt(ip,port):
    try:
        message = {"action":"get_tracker"}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        exit()

def do_nothing(ip,port):
    try:
        message = {"action":"xxx"}
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


def insert_tracker(ip,port,my_ip,my_port):
    try:
        message = {"action":"insert_tracker","ip":my_ip,"port":my_port}
        message_str = json.dumps(message)
        return connect_to(ip, port, message_str, 10)
    except:
        print "insert_tracker error"


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
        sock.sendall(str(message_str))
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
        r_name=None
        print "Download time:",float("{0:.2f}".format((t2-t1)*100)),"ms"
        if via:
            os.rename(file,"Cache/"+file)
            r_name="Cache/"+file
        else:
            os.rename(file,"Downloads/"+file)
            r_name="Downloads/"+file
        add_file_f(name,url,via=via)
        return r_name
    except:
        return None

#print download_via('localhost',3431,"sdasdasdsadsadasdas/sdas.gr")
    