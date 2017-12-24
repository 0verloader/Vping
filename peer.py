#!/usr/bin/python
import sys
sys.path.insert(0,sys.path[0]+"/modules")
from misc import initialize
import threading
from files_db import cache_clearer
from response import rel
from misc import exit_
from misc import get_local_ip,command_box
from socket_p import connect_to
import json

def get_trackers(ip,port):

    message = {"action":"get_trackers"}
    message_str = json.dumps(message)
    return connect_to(ip, port, message_str, 10)


#print get_trackers(sys.argv[2],sys.argv[3])


flags = [None]*5 #5 gia thn wra
for i in range(len(flags)):
	flags[i] = True

ip,port =initialize(get_local_ip(),sys.argv[1],sys.argv[2],sys.argv[3])

t1=threading.Thread(target=rel, args=[sys.argv[1],1,1,flags,sys.argv[1]])
t1.start()

t2=threading.Thread(target=cache_clearer, args=[flags])
t2.start()

t3 = threading.Thread(target=exit_, args=[flags,get_local_ip(),sys.argv[1]])
t3.start()
command_box(get_local_ip(),sys.argv[1],ip,port,"www.google.gr",3,"RTT","http://wroopsfun.com/wp-content/uploads/2017/12/unethical_life_hacks_11.jpg?x86721",3)

