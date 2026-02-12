import pytest
import json
from app import app, defects

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Clear defects after each test
    defects.clear()

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'total_defects' in data

def test_create_defect_success(client):
    """Test creating a defect successfully."""
    defect_data = {
        "title": "Login button not working",
        "description": "Users cannot click the login button",
        "severity": "High"
    }
    
    response = client.post('/defects', 
                          data=json.dumps(defect_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == defect_data['title']
    assert data['description'] == defect_data['description']
    assert data['severity'] == defect_data['severity']
    assert data['status'] == 'Open'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data

def test_create_defect_missing_fields(client):
    """Test creating a defect with missing fields."""
    defect_data = {
        "title": "Bug without description"
    }
    
    response = client.post('/defects',
                          data=json.dumps(defect_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_create_defect_invalid_severity(client):
    """Test creating a defect with invalid severity."""
    defect_data = {
        "title": "Test bug",
        "description": "Test description",
        "severity": "Invalid"
    }
    
    response = client.post('/defects',
                          data=json.dumps(defect_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_all_defects_empty(client):
    """Test getting all defects when none exist."""
    response = client.get('/defects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

def test_get_all_defects(client):
    """Test getting all defects."""
    # Create a defect first
    defect_data = {
        "title": "Test bug",
        "description": "Test description",
        "severity": "Medium"
    }
    client.post('/defects',
               data=json.dumps(defect_data),
               content_type='application/json')
    
    response = client.get('/defects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['title'] == defect_data['title']

def test_get_defect_by_id(client):
    """Test getting a specific defect by ID."""
    # Create a defect first
    defect_data = {
        "title": "Specific bug",
        "description": "Specific description",
        "severity": "Critical"
    }
    create_response = client.post('/defects',
                                 data=json.dumps(defect_data),
                                 content_type='application/json')
    created_defect = json.loads(create_response.data)
    defect_id = created_defect['id']
    
    # Get the defect by ID
    response = client.get(f'/defects/{defect_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == defect_id
    assert data['title'] == defect_data['title']

def test_get_defect_not_found(client):
    """Test getting a non-existent defect."""
    response = client.get('/defects/non-existent-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
