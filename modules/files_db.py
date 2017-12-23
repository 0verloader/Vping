import sqlite3
import time
import json
from random import randint
MAX_TTL=3600

def create_f():
    """A method that creates files database and its table ( files_table )
    If exception is raised program exits

    """
    try:
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS files_table(name VARCHAR,url VARCHAR PRIMARY KEY,TTL INTEGER, pswd VARCHAR);")
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False

def create_f_tr():
    try:
        conn = sqlite3.connect('.tracker_db.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS peers_table(ip VARCHAR,port INTEGER, PRIMARY KEY (ip,port));")
        conn.commit()
        c.execute("CREATE TABLE IF NOT EXISTS files_table(url VARCHAR PRIMARY KEY,ip VARCHAR,port INTEGER)")
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False
def create_f_tlt():
    try:
        conn = sqlite3.connect('.trackers.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS trackers_table(ip VARCHAR,port INTEGER,PRIMARY KEY (ip,port))")
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False

def file_search(url):
    """Fsd df."""
    try:
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        res = c.execute('SELECT * FROM files_table WHERE url="{}"'.format(url))
        res = res.fetchall()
        c.close()
        conn.close()
        if res == []:
            raise Exception("Not found")
        return res[0]
    except:
        return None

def insert_tracker_db(ip,port):
    try:
        conn = sqlite3.connect('.trackers.db')
        c = conn.cursor()
        c.execute('INSERT INTO trackers_table VALUES("{}","{}")'.format(ip,port))
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False

def insert_peer_db(ip,port):
    try:
        conn = sqlite3.connect('.tracker_db.db')
        c = conn.cursor()
        c.execute('INSERT INTO peers_table VALUES("{}","{}")'.format(ip,port))
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False

def trackers_report():
    """Fsd df."""
    try:
        conn = sqlite3.connect('.trackers.db')
        c = conn.cursor()
        res = c.execute('SELECT * FROM trackers_table')
        res = res.fetchall()
        c.close()
        conn.close()
        multikeys = []
        for i in range (0, len(res)):
            multikeys.append({ 'ip':res[i][0],'port':res[i][1]})
        message=json.dumps(multikeys)
        
        if res == []:
            raise Exception("Not found")
        return message
    except:
        return None

def peers_report():
    """Fsd df."""
    try:
        conn = sqlite3.connect('.tracker_db.db')
        c = conn.cursor()
        res = c.execute('SELECT * FROM peers_table')
        res = res.fetchall()
        c.close()
        conn.close()
        multikeys = []
        for i in range (0, len(res)):
            multikeys.append({ 'ip':res[i][0],'port':res[i][1]})
        message=json.dumps(multikeys)
        
        if res == []:
            raise Exception("Not found")
        return message
    except:
        return None


def get_tracker():
    try:
        conn = sqlite3.connect('.trackers.db')
        c = conn.cursor()
        res = c.execute('SELECT * FROM trackers_table')
        res = res.fetchall()
        c.close()
        conn.close()
        if res == []:
            raise Exception("Not found")
        rand = randint(0,len(res)-1)
        message = {"ip":res[rand][0],"port":res[rand][1]}
        message_str = json.dumps(message)
        return message_str
    except:
        return None



def cache_clearer(fl):
    """Clear the cache of files with negative ttl."""
    while fl[0]:
        time.sleep(1)
        try:
            conn = sqlite3.connect('.files.db')
            c = conn.cursor()
            c.execute('UPDATE files_table SET TTL =  TTL - 1 WHERE TTL > 0')
            conn.commit()
            res = c.execute('SELECT name,TTL FROM files_table WHERE TTL = 0')
            res = res.fetchall()
            c.execute('DELETE FROM files_table WHERE TTL = 0 ')
            conn.commit()
            for r in res:
                delete_file_os(r[0],r[1])
            c.close()
            conn.close()
        except:
            pass


def file_delete(url):
    try:
        fl=file_search(url)
        delete_file_os(fl[0],fl[2])
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute('DELETE FROM files_table WHERE url = "{}" '.format(url))
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False


def add_file(name, url, rtt, pswd=None):
    """Add a file to db."""
    try:
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute('INSERT INTO files_table VALUES("{}","{}",{},"{}")'.format(name, url, int(rtt), pswd))
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False


def update_file_time(url,n_ttl):
    try:
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute('UPDATE files_table SET TTL = {} WHERE url = "{}"'.format(n_ttl,url))
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False


def add_file_f(name, url, pswd=None, via=False):
    if file_search(url) and via:
        if file_search(url)[2]>0:
            return update_file_time(url,MAX_TTL)
        return False
    elif file_search(url) and not via:
        return update_file_time(url,-1)
    elif not file_search(url) and via:
        return add_file(name, url, MAX_TTL, pswd)
    else:
        return add_file(name, url, -1, pswd)

  
def delete_file_os(name,ttl):
    if ttl<0:
        os.remove("Downloads/"+name)
    else:
        os.remove("Cache/"+name)



def my_files():
    conn = sqlite3.connect('.files.db')
    c = conn.cursor()
    res = c.execute('SELECT * FROM files_table')
    res = res.fetchall()
    c.close()
    conn.close()
    return res

def report_files():
    res=my_files()
    multikeys = []
    for i in range (0, len(res)):
        multikeys.append({ 'name':res[i][0],'url':res[i][1]})
    message=json.dumps(multikeys)       
    print message
    return message

