import sqlite3
import time


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
        print "ssadf"
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
        return res
    except:
        return None


def cache_clearer():
    """Clear the cache of files with negative ttl."""
    while True:
        time.sleep(1)
        conn = sqlite3.connect('.files.db')
        c = conn.cursor()
        c.execute('UPDATE files_table SET TTL =  TTL - 1')
        conn.commit()
        c.execute('DELETE FROM files_table WHERE TTL = 0 ')
        conn.commit()
        c.close()
        conn.close()


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

print add_file("kostas", "sdasdsa", "55")
