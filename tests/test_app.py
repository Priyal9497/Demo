import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Employee Management System" in response.data


def test_add_page(client):
    response = client.get("/add")

    assert response.status_code == 200
    assert b"Add New Employee" in response.data


def test_employee_page(client):
    response = client.get("/employees")

    assert response.status_code == 200


def test_add_employee(client):

    response = client.post(
        "/add",
        data={
            "name": "Test User",
            "email": "test@example.com",
            "department": "IT",
            "salary": "50000"
        },
        follow_redirects=True
    )

    assert response.status_code == 200