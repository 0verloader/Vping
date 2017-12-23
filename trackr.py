#!/usr/bin/python
import sys
sys.path.insert(0,sys.path[0]+"/modules")
from misc import initialize_tr
import threading
#from files_db import cache_clearer
from response import rel3
from misc import exit_
from misc import get_local_ip

flags = [None]*5 #5 gia thn wra
for i in range(len(flags)):
	flags[i] = True

initialize_tr(get_local_ip(),sys.argv[1],sys.argv[2],sys.argv[3])

t1=threading.Thread(target=rel3, args=[sys.argv[1],flags])
t1.start()

#t2=threading.Thread(target=cache_clearer, args=[flags])
#t2.start()

t2 = threading.Thread(target=exit_, args=[flags,get_local_ip(),sys.argv[1]])
t2.start()

