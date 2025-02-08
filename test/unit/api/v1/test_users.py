import pytest

from fastapi.testclient import TestClient
from app.src.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_health_check():
   response = client.get("/v1/")
   assert response.status_code == 200

@pytest.fixture
def mock_mongo():
   with patch('app.dependencies.get_mongo_client') as mock:
       yield mock

@pytest.fixture
def mock_aws():
   with patch('app.dependencies.get_aws_client') as mock:
       yield mock

def test_create_user_success(mock_mongo):
   test_user = {
       "email": "test@test.com",
       "phone": "1234567890",
       "password": "test123"
   }
   mock_mongo.return_value.users.insert_one.return_value = MagicMock(inserted_id="123")
   
   response = client.post("/v1/users/sing-up/", json=test_user)
   assert response.status_code == 200
   assert response.json()["email"] == test_user["email"]
   assert response.json()["id"] == "123"

def test_create_user_invalid_data():
   test_user = {
       "email": "invalid-email",
       "phone": "1234567890"
   }
   response = client.post("/v1/users/sing-up/", json=test_user)
   assert response.status_code == 422