#!/usr/bin/python
import sys
sys.path.insert(0,sys.path[0]+"/modules")
from misc import initialize
import threading
from files_db import cache_clearer
from response import rel
from misc import exit_
from misc import get_local_ip

flags = [None]*5 #5 gia thn wra
for i in range(len(flags)):
	flags[i]= True

initialize(get_local_ip(),sys.argv[1])


t1=threading.Thread(target=rel, args=[sys.argv[1],1,1,flags])
t1.start()

t2=threading.Thread(target=cache_clearer, args=[flags])
t2.start()

t3 = threading.Thread(target=exit_, args=[flags,get_local_ip(),sys.argv[1]])
t3.start()