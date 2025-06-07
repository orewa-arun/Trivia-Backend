from multiprocessing import pool
from psycopg2 import pool
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import HTTPException


load_dotenv()


# Construct the DSN (Data Source Name)
dsn = os.getenv("DATABASE_URL")
# Create the connection pool
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=dsn
)


@contextmanager
def db_context():
    conn = connection_pool.getconn()
    try:
        yield conn
        conn.commit()  # Commit on success
    except Exception as e:
        conn.rollback()  # Rollback on error
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    finally:
        connection_pool.putconn(conn)  # Return connection to pool
        
        
def get_db():
    with db_context() as conn:
        yield conn