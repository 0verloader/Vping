""" Contains miscallanious functions that help the overall 
    function of running program.

    Contains:
    get_local_ip
    get_ip
    ping
    traceRT
"""
import json
import socket
import requests
import subprocess


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
