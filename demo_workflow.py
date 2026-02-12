#!/usr/bin/env python3
"""
Simple CLI demonstration of the Defect Status Workflow Management System
"""

from defect_workflow import (
    Defect, DefectManager, DefectStatus, DefectPriority, DefectWorkflow
)


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 70 + "\n")


def print_defect(defect: Defect):
    """Print defect details in a formatted way"""
    print(f"ID: {defect.id}")
    print(f"Title: {defect.title}")
    print(f"Description: {defect.description}")
    print(f"Status: {defect.status.value}")
    print(f"Priority: {defect.priority.value}")
    print(f"Created by: {defect.created_by}")
    print(f"Created at: {defect.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if defect.assigned_to:
        print(f"Assigned to: {defect.assigned_to}")
    
    if defect.status_history:
        print("\nStatus History:")
        for i, change in enumerate(defect.status_history, 1):
            print(f"  {i}. {change.from_status.value} -> {change.to_status.value}")
            print(f"     Changed by: {change.changed_by}")
            print(f"     Time: {change.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            if change.comment:
                print(f"     Comment: {change.comment}")


def demonstrate_workflow():
    """Demonstrate the defect workflow system"""
    
    print("=" * 70)
    print("DEFECT STATUS WORKFLOW MANAGEMENT SYSTEM - DEMONSTRATION")
    print("=" * 70)
    
    # Initialize the manager
    manager = DefectManager()
    
    # Scenario 1: Create a new defect
    print_separator()
    print("SCENARIO 1: Creating a new defect")
    print("-" * 70)
    
    defect1 = manager.create_defect(
        title="Login page returns 500 error",
        description="Users are unable to login. The login page returns a 500 internal server error when credentials are submitted.",
        priority=DefectPriority.CRITICAL,
        created_by="qa_team@company.com"
    )
    defect1.assign_to("john.developer@company.com")
    
    print(f"Created defect #{defect1.id}")
    print_defect(defect1)
    
    # Scenario 2: Valid workflow progression
    print_separator()
    print("SCENARIO 2: Moving defect through valid workflow states")
    print("-" * 70)
    
    print("\n1. Developer starts working (NEW -> IN_PROGRESS)")
    defect1.change_status(
        DefectStatus.IN_PROGRESS,
        "john.developer@company.com",
        "Started investigating the database connection issue"
    )
    print(f"Current status: {defect1.status.value}")
    
    print("\n2. Developer sends to testing (IN_PROGRESS -> TESTING)")
    defect1.change_status(
        DefectStatus.TESTING,
        "john.developer@company.com",
        "Fixed database connection timeout. Ready for testing."
    )
    print(f"Current status: {defect1.status.value}")
    
    print("\n3. QA marks as resolved (TESTING -> RESOLVED)")
    defect1.change_status(
        DefectStatus.RESOLVED,
        "qa_team@company.com",
        "Verified the fix. Login working correctly now."
    )
    print(f"Current status: {defect1.status.value}")
    
    print("\n4. Manager closes defect (RESOLVED -> CLOSED)")
    defect1.change_status(
        DefectStatus.CLOSED,
        "manager@company.com",
        "Issue resolved and verified. Closing."
    )
    print(f"Current status: {defect1.status.value}")
    
    print("\nFinal defect state:")
    print_defect(defect1)
    
    # Scenario 3: Defect gets reopened
    print_separator()
    print("SCENARIO 3: Reopening a closed defect")
    print("-" * 70)
    
    print("\nReopening defect due to regression (CLOSED -> REOPENED)")
    defect1.change_status(
        DefectStatus.REOPENED,
        "qa_team@company.com",
        "Issue reappeared in production. Login fails for users with special characters in username."
    )
    print(f"Current status: {defect1.status.value}")
    print_defect(defect1)
    
    # Scenario 4: Invalid transition attempt
    print_separator()
    print("SCENARIO 4: Attempting an invalid status transition")
    print("-" * 70)
    
    defect2 = manager.create_defect(
        title="Button alignment issue",
        description="Submit button is misaligned on mobile devices",
        priority=DefectPriority.LOW,
        created_by="ux_designer@company.com"
    )
    
    print(f"\nCreated defect #{defect2.id} with status: {defect2.status.value}")
    print("\nAttempting invalid transition: NEW -> RESOLVED")
    
    try:
        defect2.change_status(
            DefectStatus.RESOLVED,
            "developer@company.com",
            "Trying to skip workflow steps"
        )
    except ValueError as e:
        print(f"❌ Transition blocked! Error: {e}")
    
    print(f"\nDefect status remains: {defect2.status.value}")
    
    # Scenario 5: Viewing allowed transitions
    print_separator()
    print("SCENARIO 5: Viewing allowed transitions for different states")
    print("-" * 70)
    
    for status in DefectStatus:
        allowed = DefectWorkflow.get_allowed_transitions(status)
        allowed_str = ", ".join([s.value for s in allowed]) if allowed else "None"
        print(f"\n{status.value}:")
        print(f"  Can transition to: {allowed_str}")
    
    # Scenario 6: Filtering defects
    print_separator()
    print("SCENARIO 6: Filtering defects by status and priority")
    print("-" * 70)
    
    # Create more defects
    defect3 = manager.create_defect(
        title="API timeout",
        description="API calls timeout after 30 seconds",
        priority=DefectPriority.HIGH,
        created_by="backend_team@company.com"
    )
    defect3.change_status(DefectStatus.IN_PROGRESS, "api_dev@company.com")
    
    defect4 = manager.create_defect(
        title="Typo in footer",
        description="Copyright year is wrong",
        priority=DefectPriority.LOW,
        created_by="content_team@company.com"
    )
    
    print(f"\nTotal defects: {len(manager.get_all_defects())}")
    
    reopened = manager.get_defects_by_status(DefectStatus.REOPENED)
    print(f"\nReopened defects: {len(reopened)}")
    for d in reopened:
        print(f"  - #{d.id}: {d.title}")
    
    in_progress = manager.get_defects_by_status(DefectStatus.IN_PROGRESS)
    print(f"\nIn Progress defects: {len(in_progress)}")
    for d in in_progress:
        print(f"  - #{d.id}: {d.title}")
    
    new_defects = manager.get_defects_by_status(DefectStatus.NEW)
    print(f"\nNew defects: {len(new_defects)}")
    for d in new_defects:
        print(f"  - #{d.id}: {d.title}")
    
    high_priority = manager.get_defects_by_priority(DefectPriority.HIGH)
    print(f"\nHigh priority defects: {len(high_priority)}")
    for d in high_priority:
        print(f"  - #{d.id}: {d.title} (Status: {d.status.value})")
    
    critical_priority = manager.get_defects_by_priority(DefectPriority.CRITICAL)
    print(f"\nCritical priority defects: {len(critical_priority)}")
    for d in critical_priority:
        print(f"  - #{d.id}: {d.title} (Status: {d.status.value})")
    
    print_separator()
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_workflow()
