import sqlite3
from contextlib import contextmanager

DATABASE = "life_alert.db"

@contextmanager
def getDbConnection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()
    
