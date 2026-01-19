# SQLite / Postgres 连接
import sqlite3
from get_env import  DB_FILE

conn = sqlite3.connect(DB_FILE,check_same_thread=False)
conn.row_factory = sqlite3.Row