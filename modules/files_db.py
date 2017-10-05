import sqlite3
import time

MAX_TTL=3600

def create_f():
    """A method that creates files database and its table ( files_table )
    If exception is raised program exits

    """
    try:
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS files_table(name VARCHAR,url VARCHAR PRIMARY KEY,TTL INTEGER, pswd VARCHAR)")
        conn.commit()
        c.close()
        conn.close()
        return True
    except:
        return False

create_f()


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


def cache_clearer():
    """Clear the cache of files with negative ttl."""
    while True:
        time.sleep(1)
        try:
            conn = sqlite3.connect('.files.db')
            c = conn.cursor()
            c.execute('UPDATE files_table SET TTL =  TTL - 1')
            conn.commit()
            c.execute('DELETE FROM files_table WHERE TTL = 0 ')
            conn.commit()
            c.close()
            conn.close()
        except:
            pass


def file_delete(url):
    try:
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
