from flask import Flask, request, jsonify
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid

app = Flask(__name__)

# In-memory storage for defects
defects: Dict[str, dict] = {}

def create_defect_object(title: str, description: str, severity: str, status: str = "Open") -> dict:
    """Create a defect object with all required fields."""
    defect_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return {
        "id": defect_id,
        "title": title,
        "description": description,
        "severity": severity,
        "status": status,
        "created_at": timestamp,
        "updated_at": timestamp
    }

@app.route('/defects', methods=['POST'])
def create_defect():
    """Create a new defect."""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    required_fields = ['title', 'description', 'severity']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    # Validate severity
    valid_severities = ['Critical', 'High', 'Medium', 'Low']
    if data['severity'] not in valid_severities:
        return jsonify({
            "error": f"Invalid severity. Must be one of: {', '.join(valid_severities)}"
        }), 400
    
    # Create defect
    defect = create_defect_object(
        title=data['title'],
        description=data['description'],
        severity=data['severity'],
        status=data.get('status', 'Open')
    )
    
    defects[defect['id']] = defect
    
    return jsonify(defect), 201

@app.route('/defects', methods=['GET'])
def get_defects():
    """Get all defects with optional filtering by status and severity."""
    status_filter = request.args.get('status')
    severity_filter = request.args.get('severity')
    
    filtered_defects = list(defects.values())
    
    # Filter by status if provided
    if status_filter:
        filtered_defects = [d for d in filtered_defects if d['status'] == status_filter]
    
    # Filter by severity if provided
    if severity_filter:
        filtered_defects = [d for d in filtered_defects if d['severity'] == severity_filter]
    
    return jsonify(filtered_defects), 200

@app.route('/defects/<defect_id>', methods=['GET'])
def get_defect(defect_id: str):
    """Get a single defect by ID."""
    defect = defects.get(defect_id)
    
    if not defect:
        return jsonify({"error": "Defect not found"}), 404
    
    return jsonify(defect), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "total_defects": len(defects)
    }), 200

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
