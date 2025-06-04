import psycopg2
import psycopg2.pool  # For connection pooling
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import HTTPException


load_dotenv()


# Initialize connection pool (min 1, max 10 connections)
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
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