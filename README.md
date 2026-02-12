# Defect Management Tool - Mini Version

A lightweight REST API for managing software defects built with Python Flask.

## Features

- ✅ Create new defects
- ✅ Get all defects
- ✅ Get a specific defect by ID
- ✅ In-memory storage (no database required)
- ✅ Comprehensive test coverage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MarckPetersen/Defect-management-tool-mini-version-.git
cd Defect-management-tool-mini-version-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "total_defects": 0
}
```

### Create Defect
```
POST /defects
Content-Type: application/json

{
  "title": "Login button not working",
  "description": "Users cannot click the login button on the homepage",
  "severity": "High",
  "status": "Open"
}
```

**Required fields:**
- `title` (string): Brief description of the defect
- `description` (string): Detailed description
- `severity` (string): Must be one of: `Critical`, `High`, `Medium`, `Low`

**Optional fields:**
- `status` (string): Default is `Open`

Response (201 Created):
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Login button not working",
  "description": "Users cannot click the login button on the homepage",
  "severity": "High",
  "status": "Open",
  "created_at": "2026-02-12T12:00:00.000000Z",
  "updated_at": "2026-02-12T12:00:00.000000Z"
}
```

### Get All Defects
```
GET /defects
```

Response (200 OK):
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Login button not working",
    "description": "Users cannot click the login button on the homepage",
    "severity": "High",
    "status": "Open",
    "created_at": "2026-02-12T12:00:00.000000Z",
    "updated_at": "2026-02-12T12:00:00.000000Z"
  }
]
```

### Get Defect by ID
```
GET /defects/{defect_id}
```

Response (200 OK):
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Login button not working",
  "description": "Users cannot click the login button on the homepage",
  "severity": "High",
  "status": "Open",
  "created_at": "2026-02-12T12:00:00.000000Z",
  "updated_at": "2026-02-12T12:00:00.000000Z"
}
```

Response (404 Not Found):
```json
{
  "error": "Defect not found"
}
```

## Running Tests

Run the test suite:
```bash
pytest test_app.py -v
```

## Example Usage

Using curl:

```bash
# Create a defect
curl -X POST http://localhost:5000/defects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Database connection timeout",
    "description": "Application fails to connect to database after 30 seconds",
    "severity": "Critical"
  }'

# Get all defects
curl http://localhost:5000/defects

# Get a specific defect
curl http://localhost:5000/defects/{defect_id}
```

## Technical Details

- **Framework:** Flask 3.0.0
- **Testing:** pytest 7.4.3
- **Storage:** In-memory (data is lost when server restarts)
- **Authentication:** None (for demo purposes)

## License

MIT