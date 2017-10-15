""" Contains miscallanious functions that help the overall 
    function of running program.

    Contains:
    get_local_ip
    get_ip
    ping
    traceRT
"""
import threading
import json
import socket
import requests
import subprocess
import urllib
import os
import time
from socket_p import get_metrics
import Queue

def get_local_ip():
    """Return my local ip if nat otherwise ipv4."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        ip = (s.getsockname()[0])
        s.close()
        return ip
    except:
        return None


def get_ip():
    """Return my ipv4."""
    try:
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        ip = j['ip']
        return ip
    except:
        return None


def ping(input, number, pin, index):
    """A method that pings to ip = input
    If it fails returns -1
    """
    try:
        ping = subprocess.check_output(["ping", "-c", number, input])
        ping = (ping.split('/'))
        pin[index] = float(ping[-3])
    except:
        pin[index] = None


def traceRT(input, pin, index):

    """A method that traceroutes the ip = input
    If it fails returns -1
    """
    try:
        trace = subprocess.check_output(["traceroute", input])
        trace = trace.split('\n')
        trace = trace[-2]
        last = trace
        trace = trace.split(' ')
        last = last.split('(')
        num = len(last) - 1

        if(num > 1):
            last2 = last[2]

        if(num > 2):
            last3 = last[3]

        if(num > 0):
            last = last[1]

        if(num > 0):
            last = last.split(')')
            last = last[0]

        if(num > 1):
            last2 = last2.split(')')
            last2 = last2[0]

        if(num > 2):
            last3 = last3.split(')')
            last3 = last3[0]

        if(trace[2] == '*' and trace[3] == '*' and trace[4] == '*' or (last != input and last2!=input and last3!=input)):
            raise Exception("Traceroute failed")
        elif(trace[0] != ''):
            pin[index] = int(trace[0])
        else:
            pin[index] = int(trace[1])
    except:
        pin[index] = None

   
def find_full_path(ip,port,ip_end,no_of_pings,array,index,url):
    results=[None]*3
    """
    socket_T=threading.Thread(target=get_metrics, args=[ip,port,no_of_pings,url,results,0])
    socket_T.start()
    ping_T=threading.Thread(target=ping, args=[ip,no_of_pings,results,1])
    ping_T.start()
    trace_T=threading.Thread(target=traceRT, args=[ip,results,2])
    trace_T.start()

    socket_T.join()
    ping_T.join()
    trace_T.join()

    if(results[0][0]==None or results[1]==None):
        path_Ping=None
    else:
        path_Ping=results[0][0]+results[1]

    if(results[0][1]==None or results[2]==None):
        path_Trace=None
    else:
        path_Trace=results[0][1]+results[2]
    
    array[index] = path_Ping,path_Trace
    """
    array[index]=5,6
    return True


def find_all(nodes_array,ip_end,no_of_pings,url,par_threads):
    results=[None]*(len(nodes_array)+1)
    direct=[None]*2
    
    for ii in range(0,len(nodes_array), par_threads):
        if(ii+par_threads  < len(nodes_array)):
            threads=[None]*par_threads
            for yy in range(ii,ii+par_threads):
                threads[yy-ii]=threading.Thread(target=find_full_path, args=[nodes_array[yy][0],nodes_array[yy][1],ip_end,no_of_pings,results,yy,url])
                threads[yy-ii].start()
            for yy in range(ii,ii+par_threads):
                threads[yy-ii].join()
        else:
            threads=[None]*(len(nodes_array)-ii)
            for yy in range(ii,len(nodes_array)):
                threads[yy-ii]=threading.Thread(target=find_full_path, args=[nodes_array[yy][0],nodes_array[yy][1],ip_end,no_of_pings,results,yy,url])
                threads[yy-ii].start()
            for yy in range(ii,len(nodes_array)):
                threads[yy-ii].join()

    direct_Ping=threading.Thread(target=ping, args=[ip_end,no_of_pings,direct,0])
    direct_Ping.start()
    direct_Trace=threading.Thread(target=traceRT, args=[ip_end,direct,1])
    direct_Trace.start()

    direct_Trace.join()
    direct_Ping.join()
    results[len(nodes_array)]=direct
    return results


aa=[('432.243.2',1),('432.243.2',2),('432.243.2',3)]

print find_all(aa,"dsdadas",4,"dasdasdassadasd",2)


def find_Best(ip_node_array,node_port_array,ip_end,no_of_pings,filter,url):
    table=find_all(ip_node_array,node_port_array,ip_end,no_of_pings,url)
    num=len(ip_node_array)
    ind_n=0
    if DEBUGGING==1:
        print ''
        print " Index.\t\t\tRTT   / HOPS"
        for ii in range(0,num):
            print " Ind",ind_n,":\t\t",table[ii][0],"/",table[ii][1]
            ind_n=ind_n+1
        print " Direct:\t\t",table[num][0],"/",table[num][1]

    if os.path.exists(".metrics_history.csv"):
        with open('.metrics_history.csv','a') as f:
            w=csv.writer(f,delimiter=',')
            for i in range(0,num):
                w.writerow([ip_node_array[i],node_port_array[i],table[i][0],table[i][1],url])
            w.writerow([ip_end,80,table[num][0],table[num][1],url])
    else:
        with open('.metrics_history.csv','wb+') as f:
            writer = csv.writer(f)
            writer.writerow(["ip", "port", "rtt", "hops","url"])
            w=csv.writer(f,delimiter=',')
            for i in range(0,num):
                w.writerow([ip_node_array[i],node_port_array[i],table[i][0],table[i][1],url])
            w.writerow([ip_end,80,table[num][0],table[num][1],url])

    que = Queue.Queue()
    min_Ping=-5
    min_Trace=-5
    ping_Index=-5
    trace_Index=-5
    for ii in range(0,num+1):
        if table[ii][0]>0:
            min_Ping=table[ii][0]
            ping_Index=ii
            break
    for ii in range(0,num+1):
        if table[ii][1]>0:
            min_Trace=table[ii][1]
            trace_Index=ii
            break
    if(filter=="RTT" and ping_Index==-5):
        if DEBUGGING==1:
            print "None ping was successful. Filter has changed to \"HOPS\""
        filter="HOPS"
    if(filter=="HOPS" and trace_Index==-5):
        if DEBUGGING==1:
            print "None traceroute was successful. Filter has changed to \"RTT\""
        filter="RTT"

    if(filter=="RTT"):
        if(ping_Index==-5):
            if DEBUGGING==1:
                print "No way to connect to server. Please try again later"
            return
        for ii in range(0,num+1):
            if((table[ii][0]>0 ) and ( table[ii][0]<min_Ping)):
                min_Ping=table[ii][0]
                ping_Index=ii
        ammOfQue=0
        for ii in range(0,num+1):
            if table[ii][0]==min_Ping:
                temp=table[ii][1],ii
                que.put(temp)
                ammOfQue=ammOfQue+1
        if(ammOfQue==1):
            return ping_Index
        if DEBUGGING==1:
            print "Many routes with the same min ping have been found."

        temp=[None]*ammOfQue
        for ii in range(0,ammOfQue):
            temp[ii]=que.get()
        min_temp=-5
        ind_temp=-5
        for ii in range(0,ammOfQue):
            if(temp[ii][0]>0):
                ind_temp=ii
                min_temp=temp[ii][0]
                break
        if(ind_temp<0):
            return temp[0][1]
        else:
            for ii in range(0,ammOfQue):
                if temp[ii][0]>0 and temp[ii][0]<min_temp:
                    min_temp=temp[ii][0]
                    ind_temp=ii
            return ind_temp

    elif filter=="HOPS":
        if(trace_Index==-5):
            print "No way to connect to server. Please try again later"
            return
        for ii in range(0,num+1):
            if((table[ii][1] > 0 ) and (table[ii][1] < min_Trace)):
                min_Trace=table[ii][1]
                trace_Index=ii
        ammOfQue=0
        for ii in range(0,num+1):
            if table[ii][1]==min_Trace:
                temp=table[ii][0],ii
                que.put(temp)
                ammOfQue=ammOfQue+1
        if(ammOfQue==1):
            return trace_Index
        if DEBUGGING==1:
            print "Many routes with the same min traceroute have been found."
        temp=[None]*ammOfQue
        for ii in range(0,ammOfQue):
            temp[ii]=que.get()
        min_temp=-5
        ind_temp=-5
        for ii in range(0,ammOfQue):
            if(temp[ii][0]>0):
                ind_temp=ii
                min_temp=temp[ii][0]
                break
        if(ind_temp<0):
            return temp[0][1]
        else:
            for ii in range(0,ammOfQue):
                if temp[ii][0]>0 and temp[ii][0]<min_temp:
                    min_temp=temp[ii][0]
                    ind_temp=ii
            return ind_temp


def find_Best_F(ip_node_array,node_port_array,ip_end,no_of_pings,filter,url):
    res=find_Best(ip_node_array,node_port_array,ip_end,no_of_pings,filter,url)
    num=len(ip_node_array)
    return res