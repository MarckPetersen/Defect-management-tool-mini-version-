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

def test_filter_defects_by_status(client):
    """Test filtering defects by status."""
    # Create defects with different statuses
    defect1 = {
        "title": "Open Bug",
        "description": "This is an open bug",
        "severity": "High",
        "status": "Open"
    }
    defect2 = {
        "title": "Closed Bug",
        "description": "This is a closed bug",
        "severity": "Medium",
        "status": "Closed"
    }
    defect3 = {
        "title": "In Progress Bug",
        "description": "This is in progress",
        "severity": "Critical",
        "status": "In Progress"
    }
    
    client.post('/defects', data=json.dumps(defect1), content_type='application/json')
    client.post('/defects', data=json.dumps(defect2), content_type='application/json')
    client.post('/defects', data=json.dumps(defect3), content_type='application/json')
    
    # Filter by status=Open
    response = client.get('/defects?status=Open')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['status'] == 'Open'
    assert data[0]['title'] == 'Open Bug'
    
    # Filter by status=Closed
    response = client.get('/defects?status=Closed')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['status'] == 'Closed'
    assert data[0]['title'] == 'Closed Bug'

def test_filter_defects_by_severity(client):
    """Test filtering defects by severity."""
    # Create defects with different severities
    defect1 = {
        "title": "Critical Bug",
        "description": "Critical issue",
        "severity": "Critical"
    }
    defect2 = {
        "title": "High Bug",
        "description": "High priority issue",
        "severity": "High"
    }
    defect3 = {
        "title": "Medium Bug",
        "description": "Medium priority issue",
        "severity": "Medium"
    }
    defect4 = {
        "title": "Low Bug",
        "description": "Low priority issue",
        "severity": "Low"
    }
    
    client.post('/defects', data=json.dumps(defect1), content_type='application/json')
    client.post('/defects', data=json.dumps(defect2), content_type='application/json')
    client.post('/defects', data=json.dumps(defect3), content_type='application/json')
    client.post('/defects', data=json.dumps(defect4), content_type='application/json')
    
    # Filter by severity=Critical
    response = client.get('/defects?severity=Critical')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['severity'] == 'Critical'
    assert data[0]['title'] == 'Critical Bug'
    
    # Filter by severity=High
    response = client.get('/defects?severity=High')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['severity'] == 'High'

def test_filter_defects_by_status_and_severity(client):
    """Test filtering defects by both status and severity."""
    # Create defects with various combinations
    defect1 = {
        "title": "Open Critical Bug",
        "description": "Open and critical",
        "severity": "Critical",
        "status": "Open"
    }
    defect2 = {
        "title": "Open High Bug",
        "description": "Open and high",
        "severity": "High",
        "status": "Open"
    }
    defect3 = {
        "title": "Closed Critical Bug",
        "description": "Closed and critical",
        "severity": "Critical",
        "status": "Closed"
    }
    
    client.post('/defects', data=json.dumps(defect1), content_type='application/json')
    client.post('/defects', data=json.dumps(defect2), content_type='application/json')
    client.post('/defects', data=json.dumps(defect3), content_type='application/json')
    
    # Filter by status=Open and severity=Critical
    response = client.get('/defects?status=Open&severity=Critical')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['status'] == 'Open'
    assert data[0]['severity'] == 'Critical'
    assert data[0]['title'] == 'Open Critical Bug'

def test_filter_defects_no_matches(client):
    """Test filtering defects with no matches."""
    # Create a defect
    defect1 = {
        "title": "Open Bug",
        "description": "This is an open bug",
        "severity": "High",
        "status": "Open"
    }
    client.post('/defects', data=json.dumps(defect1), content_type='application/json')
    
    # Filter by non-existent status
    response = client.get('/defects?status=NonExistent')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0
    assert data == []
