from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "namesdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.get("/hello")
def hello(name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS names (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cur.execute("INSERT INTO names (name) VALUES (%s)", (name,))
    conn.commit()

    cur.close()
    conn.close()

    return {"message": f"Hello {name}"}


@app.get("/names")
def get_names():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS names (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cur.execute("SELECT name FROM names ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"names": [row[0] for row in rows]}