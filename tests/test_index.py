"""Tests for '/' endpoint."""

def test_success(client):
    """Success test."""
    response = client.get("/")
    assert response.status_code == 200
