""" DB access."""

from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from . import settings


@contextmanager
def connect():
    """Connect to DB and return connection."""
    conn = psycopg2.connect(settings.DB_URL)
    try:
        yield conn
    finally:
        conn.close()


def execute(sql, params=None):
    """Execute sql statement and commit changes."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()


def insert(sql, params=None):
    """Execute sql and returns one value.

    Usually sql has formar:
    INSERT INTO table (...) VALUES (...) RETURNING id;
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()
            return cur.fetchone()[0]


def fetchall(sql, params=None, conn=None):
    """Execute sql statemnt and returns all found records.

    If conn is not provider, the new connection will be used."""
    def _run(conn):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return list(cur.fetchall())

    if conn is None:
        with connect() as cn1:
            return _run(cn1)
    else:
        return _run(conn)


def fetchval(sql, params=None, conn=None):
    """Execute sql statemnt and returns scalar value.

    If conn is not provider, the new connection will be used."""
    def _run(conn):
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = list(cur.fetchall())
            if not rows:
                return None
            return rows[0][0]

    if conn is None:
        with connect() as cn1:
            return _run(cn1)
    else:
        return _run(conn)
