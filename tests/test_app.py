import sys
import os
import json
import pytest

# Adding project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Flask Application Running"

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    users = response.get_json()
    assert isinstance(users, list)
    assert len(users) >= 1

def test_create_user_success(client):
    new_user = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "test1234"
    }
    response = client.post('/users', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert "User created successfully" in data["message"]

def test_create_user_invalid_password(client):
    new_user = {
        "name": "Bad User",
        "email": "baduser@example.com",
        "password": "12345"
    }
    response = client.post('/users', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "Password" in data["error"]

def test_login_success(client):
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"

def test_login_failure(client):
    login_data = {
        "email": "john@example.com",
        "password": "wrongpassword"
    }
    response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 401
    data = response.get_json()
    assert data["status"] == "failed"
