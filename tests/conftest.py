"""Conftest file for pytest."""

import os

import pytest

import app.db as app_db
from app import cli, settings
from app.main import app


@pytest.fixture
def client():
    """Test client."""
    with app.test_client() as clt:
        yield clt


@pytest.fixture
def db(monkeypatch):
    """Intiialize DB."""
    db_url = os.getenv("TEST_DB_URL")
    if db_url is None:
        raise Exception("Please define environment variable TEST_DB_URL for test db")
    monkeypatch.setattr(settings, "DB_URL", db_url)
    cli.create_tables()
    with app_db.connect() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO QuestionTypes(code) VALUES (%s);",
                [["multi"], ["single"], ["freetext"]],
            )
            conn.commit()
