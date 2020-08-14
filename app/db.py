from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from . import settings


@contextmanager
def connect():
    conn = psycopg2.connect(settings.DB_URL)
    try:
        yield conn
    finally:
        conn.close()


def execute(sql, params=None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()


def insert(sql, params=None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()
            return cur.fetchone()[0]


def fetchall(sql, params=None, conn=None):
    def _run(conn):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return list(cur.fetchall())

    if conn is None:
        with connect() as conn:
            return _run(conn)
    else:
        return _run(conn)


def fetchval(sql, params=None, conn=None):
    def _run(conn):
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = list(cur.fetchall())
            if not rows:
                return None
            return rows[0][0]

    if conn is None:
        with connect() as conn:
            return _run(conn)
    else:
        return _run(conn)
