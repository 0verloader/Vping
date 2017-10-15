import threading
import socket
import json
RECV_BUFFER_SIZE=1024
from files_db import report_files
from misc import get_local_ip,metr
from files_db import file_search
from socket_p import download_directly
import sys

def newSocket(conn,c_add,trip,trport):
    while True:
        data = conn.recv(RECV_BUFFER_SIZE)
        if data:
            data=json.loads(data)
            if data['action'] == "get_files":
                message=report_files()
                conn.sendall(message)
            elif data['action'] == "get_metrics":
                message=metr(trip,trport,10,get_local_ip(),sys.argv[1])
                conn.sendall(message)
            elif data['action'] == "get_metrics":
                if(file_search(data['url'])!=None):
                    message = {"ping":0,"RTT":0}
                    message_str = json.dumps(message)
                    conn.sendall(message_str)
                else:
                    res=[None]*2
                    zPing=threading.Thread(target=misc.ping, args=[data['ip_end'],data['no_of_pings'],res,0])
                    zPing.start()
                    zTrace=threading.Thread(target=misc.traceRT, args=[data['ip_end'],res,1])
                    zTrace.start()
                    zPing.join()
                    zTrace.join()
                    message = {"ping":res[0],"RTT":res[1]}
                    message_str = json.dumps(message)
                    conn.sendall(message_str)
            elif data['action'] == "download_via":
                fl = file_search(data['url'])
                if(fl !=None):
                    print "sdsd"
                    if fl[2]>0:
                        fl="Cache/"+fl[0]
                    else:
                        fl="Downloads/"+fl[0]
                    f=open(fl)
                else:
                    file = download_directly(data['url'],True)
                    f = open(file)
                l=f.read(1024)
                while(l):
                    conn.send(l)
                    l=f.read(1024)
                conn.send("<EOF>")
            elif data['action'] == "xxx":
                message = {"answer":"ok"}
                message_str = json.dumps(message)
                conn.sendall(message_str)
        else:
            break
    

def rel(port,trackrIp,trackrPort,f):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', int(port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        sock.listen(10)
        while f[0] is True:
            connection, client_address = sock.accept()
            t =threading.Thread(target=newSocket, args=(connection,client_address,trackrIp,trackrPort))
            t.start()
    except:
        print "Relay service terminated"
    finally:
        print "Relay node is dead!"


