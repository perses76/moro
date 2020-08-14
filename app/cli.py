import os
import psycopg2
from . import settings


def create_tables():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    init_db_path = os.path.join(folder_path, 'init_db.sql')
    with open(init_db_path) as f:
        init_db_sql = f.read()
    conn = psycopg2.connect(settings.DB_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(init_db_sql)
            conn.commit()
    finally:
        conn.close()

def init_db():
    create_tables()
    folder_path = os.path.abspath(os.path.dirname(__file__))
    sample_data_path = os.path.join(folder_path, 'sample_data.sql')
    with open(sample_data_path) as f:
        sample_data_sql = f.read()
    conn = psycopg2.connect(settings.DB_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(sample_data_sql)
            conn.commit()
    finally:
        conn.close()
