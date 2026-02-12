# Defect Management Tool - Mini Version

A Python-based defect management system with comprehensive status workflow logic. This tool enforces valid state transitions, maintains complete audit trails, and provides a clean API for managing defects through their lifecycle.

## Features

✅ **Status Workflow Management** - Structured defect lifecycle with enforced state transitions  
✅ **Complete Audit Trail** - Track all status changes with timestamps and user information  
✅ **Priority Management** - Categorize defects by priority (Low, Medium, High, Critical)  
✅ **Validation** - Prevent invalid workflow transitions  
✅ **Filtering & Querying** - Find defects by status, priority, or other attributes  
✅ **Zero Dependencies** - Uses only Python standard library  

## Quick Start

```bash
# Run the demonstration
python demo_workflow.py

# Run tests
python -m unittest test_defect_workflow -v
```

## Workflow States

**NEW** → **IN PROGRESS** → **TESTING** → **RESOLVED** → **CLOSED**  
                                                ↓  
                                           **REOPENED** ↩

See [WORKFLOW_DOCUMENTATION.md](WORKFLOW_DOCUMENTATION.md) for complete documentation.

## Basic Usage

```python
from defect_workflow import DefectManager, DefectStatus, DefectPriority

# Create manager and defect
manager = DefectManager()
defect = manager.create_defect(
    title="Login error",
    description="500 error on login",
    priority=DefectPriority.CRITICAL,
    created_by="qa@company.com"
)

# Move through workflow
defect.change_status(DefectStatus.IN_PROGRESS, "dev@company.com", "Working on fix")
defect.change_status(DefectStatus.TESTING, "dev@company.com", "Ready for test")
defect.change_status(DefectStatus.RESOLVED, "qa@company.com", "Tests passed")
```

## Project Files

- `defect_workflow.py` - Core implementation of workflow logic
- `test_defect_workflow.py` - Comprehensive unit tests (23 test cases)
- `demo_workflow.py` - Interactive demonstration with examples
- `WORKFLOW_DOCUMENTATION.md` - Complete API reference and documentation

## Testing

All 23 unit tests pass with 100% success rate, covering:
- Valid and invalid state transitions
- Status history tracking
- Defect filtering and querying
- Error handling and edge cases