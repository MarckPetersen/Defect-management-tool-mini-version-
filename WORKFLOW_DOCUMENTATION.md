# Defect Status Workflow Logic

This project implements a comprehensive defect management system with status workflow logic. The system enforces valid state transitions and maintains a complete history of status changes for each defect.

## Features

- **Structured Workflow States**: Defects move through well-defined states (New, In Progress, Testing, Resolved, Closed, Reopened)
- **Transition Validation**: The system enforces valid state transitions and prevents invalid workflow jumps
- **Status History Tracking**: Complete audit trail of all status changes with timestamps and user information
- **Priority Management**: Defects can be assigned different priority levels (Low, Medium, High, Critical)
- **Defect Assignment**: Defects can be assigned to specific users
- **Filtering Capabilities**: Query defects by status, priority, or other attributes

## Workflow States

The defect workflow includes the following states:

1. **New**: Initial state when a defect is created
2. **In Progress**: Developer is actively working on the defect
3. **Testing**: Fix is ready for QA testing
4. **Resolved**: Testing passed, waiting for final closure
5. **Closed**: Defect is fully resolved and closed
6. **Reopened**: Previously closed defect that needs to be addressed again

## Valid State Transitions

The system enforces the following workflow transitions:

```
NEW → In Progress, Closed
IN_PROGRESS → Testing, New, Closed
TESTING → Resolved, In Progress, Reopened
RESOLVED → Closed, Reopened
CLOSED → Reopened
REOPENED → In Progress, Closed
```

Any attempt to make an invalid transition will raise a `ValueError` with information about allowed transitions.

## Installation

No external dependencies required. This project uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/MarckPetersen/Defect-management-tool-mini-version-.git
cd Defect-management-tool-mini-version-
```

## Usage

### Basic Example

```python
from defect_workflow import DefectManager, DefectStatus, DefectPriority

# Create a defect manager
manager = DefectManager()

# Create a new defect
defect = manager.create_defect(
    title="Login button not working",
    description="Users cannot click the login button",
    priority=DefectPriority.HIGH,
    created_by="qa@company.com"
)

# Assign the defect
defect.assign_to("developer@company.com")

# Change status (following valid workflow)
defect.change_status(
    DefectStatus.IN_PROGRESS,
    changed_by="developer@company.com",
    comment="Started investigating the issue"
)

# Continue workflow
defect.change_status(DefectStatus.TESTING, "developer@company.com", "Fix ready for testing")
defect.change_status(DefectStatus.RESOLVED, "qa@company.com", "Tests passed")
defect.change_status(DefectStatus.CLOSED, "manager@company.com", "Closing verified fix")

# View status history
for change in defect.get_status_history():
    print(f"{change.from_status.value} -> {change.to_status.value} by {change.changed_by}")
```

### Filtering Defects

```python
# Get all defects with a specific status
new_defects = manager.get_defects_by_status(DefectStatus.NEW)
in_progress = manager.get_defects_by_status(DefectStatus.IN_PROGRESS)

# Get defects by priority
critical_defects = manager.get_defects_by_priority(DefectPriority.CRITICAL)

# Get all defects
all_defects = manager.get_all_defects()
```

### Checking Allowed Transitions

```python
from defect_workflow import DefectWorkflow, DefectStatus

# Check if a transition is valid
is_valid = DefectWorkflow.is_valid_transition(
    DefectStatus.NEW, 
    DefectStatus.IN_PROGRESS
)  # Returns True

# Get all allowed transitions from a status
allowed = DefectWorkflow.get_allowed_transitions(DefectStatus.NEW)
# Returns [DefectStatus.IN_PROGRESS, DefectStatus.CLOSED]
```

## Running the Demo

See the workflow system in action:

```bash
python demo_workflow.py
```

This demonstrates:
- Creating defects
- Moving through valid workflow states
- Reopening closed defects
- Invalid transition handling
- Filtering and querying defects

## Running Tests

The project includes comprehensive unit tests:

```bash
python -m unittest test_defect_workflow -v
```

Test coverage includes:
- Valid and invalid state transitions
- Defect creation and management
- Status history tracking
- Filtering operations
- Edge cases and error handling

## API Reference

### Classes

#### `DefectStatus`
Enum of all possible defect statuses.

#### `DefectPriority`
Enum of defect priority levels.

#### `DefectWorkflow`
Static class that defines and validates workflow transitions.

**Methods:**
- `is_valid_transition(from_status, to_status)`: Check if a transition is valid
- `get_allowed_transitions(status)`: Get list of allowed target statuses

#### `Defect`
Represents a single defect.

**Properties:**
- `id`: Unique identifier
- `title`: Brief description
- `description`: Detailed description
- `priority`: Priority level
- `status`: Current status
- `created_by`: Creator's identifier
- `created_at`: Creation timestamp
- `assigned_to`: Assigned user (optional)
- `status_history`: List of status changes

**Methods:**
- `change_status(new_status, changed_by, comment)`: Change defect status
- `assign_to(user)`: Assign defect to a user
- `get_status_history()`: Get copy of status history

#### `DefectManager`
Manages collection of defects.

**Methods:**
- `create_defect(title, description, priority, created_by)`: Create new defect
- `get_defect(defect_id)`: Retrieve defect by ID
- `update_defect_status(defect_id, new_status, changed_by, comment)`: Update status
- `get_defects_by_status(status)`: Filter by status
- `get_defects_by_priority(priority)`: Filter by priority
- `get_all_defects()`: Get all defects

#### `StatusChange`
Records a single status change event.

**Properties:**
- `from_status`: Previous status
- `to_status`: New status
- `changed_by`: User who made the change
- `timestamp`: When the change occurred
- `comment`: Optional comment about the change

## Project Structure

```
.
├── README.md                    # Project overview
├── WORKFLOW_DOCUMENTATION.md    # This documentation
├── defect_workflow.py           # Main implementation
├── test_defect_workflow.py      # Unit tests
└── demo_workflow.py             # Interactive demonstration
```

## Design Decisions

1. **Immutable Status History**: Status changes are recorded and cannot be modified, providing a complete audit trail.

2. **Strict Workflow Enforcement**: Invalid transitions raise exceptions rather than silently failing, ensuring data integrity.

3. **Minimal Dependencies**: Uses only Python standard library for maximum portability.

4. **Enum-based States**: Using enums for statuses and priorities provides type safety and prevents invalid values.

5. **Separation of Concerns**: Workflow logic is separate from defect management, allowing easy modification of workflow rules.

## Future Enhancements

Potential improvements for future versions:
- Persistence layer (database integration)
- User authentication and authorization
- Email notifications on status changes
- Custom workflow configurations
- REST API interface
- Web-based UI
- Defect attachments and comments
- Time tracking
- Sprint/milestone management

## License

This project is provided as-is for educational and demonstration purposes.

## Contributing

This is a mini version for demonstration. For a production system, consider:
- Adding proper error handling
- Implementing persistence
- Adding authentication/authorization
- Creating a proper API layer
- Adding more comprehensive validation
