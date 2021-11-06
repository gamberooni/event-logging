import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from config import *
from utils.utils import init_postgres_conn

init_schema_sql = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    sent_at TIMESTAMP,
    sender VARCHAR(100),
    text TEXT,
    recipient VARCHAR(100)
);
"""

def main():
    # initialize connection to postgres
    conn = init_postgres_conn(
        postgres_host,
        postgres_port,
        postgres_database,
        postgres_user,
        postgres_password,
    )
    
    cur = conn.cursor() # create a cursor

    cur.execute(init_schema_sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
