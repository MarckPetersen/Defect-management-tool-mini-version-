"""
Defect Status Workflow Management System

This module implements a defect management system with workflow logic
for tracking and managing defects through various states.
"""

from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional


class DefectStatus(Enum):
    """Enumeration of all possible defect statuses"""
    NEW = "New"
    IN_PROGRESS = "In Progress"
    TESTING = "Testing"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    REOPENED = "Reopened"


class DefectPriority(Enum):
    """Enumeration of defect priorities"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class DefectWorkflow:
    """
    Defines the valid status transitions in the defect workflow
    """
    
    # Define valid state transitions
    VALID_TRANSITIONS = {
        DefectStatus.NEW: [DefectStatus.IN_PROGRESS, DefectStatus.CLOSED],
        DefectStatus.IN_PROGRESS: [DefectStatus.TESTING, DefectStatus.NEW, DefectStatus.CLOSED],
        DefectStatus.TESTING: [DefectStatus.RESOLVED, DefectStatus.IN_PROGRESS, DefectStatus.REOPENED],
        DefectStatus.RESOLVED: [DefectStatus.CLOSED, DefectStatus.REOPENED],
        DefectStatus.CLOSED: [DefectStatus.REOPENED],
        DefectStatus.REOPENED: [DefectStatus.IN_PROGRESS, DefectStatus.CLOSED]
    }
    
    @classmethod
    def is_valid_transition(cls, from_status: DefectStatus, to_status: DefectStatus) -> bool:
        """
        Check if a transition from one status to another is valid
        
        Args:
            from_status: Current defect status
            to_status: Target defect status
            
        Returns:
            True if transition is valid, False otherwise
        """
        if from_status not in cls.VALID_TRANSITIONS:
            return False
        return to_status in cls.VALID_TRANSITIONS[from_status]
    
    @classmethod
    def get_allowed_transitions(cls, status: DefectStatus) -> List[DefectStatus]:
        """
        Get list of allowed transitions from a given status
        
        Args:
            status: Current defect status
            
        Returns:
            List of valid target statuses
        """
        return cls.VALID_TRANSITIONS.get(status, [])


class StatusChange:
    """Represents a single status change in defect history"""
    
    def __init__(self, from_status: DefectStatus, to_status: DefectStatus, 
                 changed_by: str, comment: str = ""):
        self.from_status = from_status
        self.to_status = to_status
        self.changed_by = changed_by
        self.timestamp = datetime.now()
        self.comment = comment
    
    def __repr__(self):
        return (f"StatusChange({self.from_status.value} -> {self.to_status.value}, "
                f"by {self.changed_by} at {self.timestamp})")


class Defect:
    """
    Represents a defect with status workflow management
    """
    
    _id_counter = 1
    
    def __init__(self, title: str, description: str, priority: DefectPriority, 
                 created_by: str):
        """
        Initialize a new defect
        
        Args:
            title: Brief description of the defect
            description: Detailed description of the defect
            priority: Priority level of the defect
            created_by: User who created the defect
        """
        self.id = Defect._id_counter
        Defect._id_counter += 1
        self.title = title
        self.description = description
        self.priority = priority
        self.status = DefectStatus.NEW
        self.created_by = created_by
        self.created_at = datetime.now()
        self.assigned_to: Optional[str] = None
        self.status_history: List[StatusChange] = []
    
    def change_status(self, new_status: DefectStatus, changed_by: str, 
                     comment: str = "") -> bool:
        """
        Change the status of the defect
        
        Args:
            new_status: Target status
            changed_by: User making the change
            comment: Optional comment about the change
            
        Returns:
            True if status change was successful, False otherwise
            
        Raises:
            ValueError: If the transition is invalid
        """
        if not DefectWorkflow.is_valid_transition(self.status, new_status):
            raise ValueError(
                f"Invalid transition from {self.status.value} to {new_status.value}. "
                f"Allowed transitions: {[s.value for s in DefectWorkflow.get_allowed_transitions(self.status)]}"
            )
        
        # Record the status change
        status_change = StatusChange(self.status, new_status, changed_by, comment)
        self.status_history.append(status_change)
        
        # Update the status
        old_status = self.status
        self.status = new_status
        
        return True
    
    def assign_to(self, user: str):
        """Assign the defect to a user"""
        self.assigned_to = user
    
    def get_status_history(self) -> List[StatusChange]:
        """Get the complete status change history"""
        return self.status_history.copy()
    
    def __repr__(self):
        return (f"Defect(id={self.id}, title='{self.title}', "
                f"status={self.status.value}, priority={self.priority.value})")


class DefectManager:
    """
    Manages a collection of defects and enforces workflow rules
    """
    
    def __init__(self):
        self.defects: Dict[int, Defect] = {}
    
    def create_defect(self, title: str, description: str, priority: DefectPriority,
                     created_by: str) -> Defect:
        """
        Create a new defect
        
        Args:
            title: Brief description of the defect
            description: Detailed description of the defect
            priority: Priority level of the defect
            created_by: User creating the defect
            
        Returns:
            The created Defect object
        """
        defect = Defect(title, description, priority, created_by)
        self.defects[defect.id] = defect
        return defect
    
    def get_defect(self, defect_id: int) -> Optional[Defect]:
        """Get a defect by its ID"""
        return self.defects.get(defect_id)
    
    def update_defect_status(self, defect_id: int, new_status: DefectStatus,
                           changed_by: str, comment: str = "") -> bool:
        """
        Update the status of a defect
        
        Args:
            defect_id: ID of the defect to update
            new_status: Target status
            changed_by: User making the change
            comment: Optional comment about the change
            
        Returns:
            True if update was successful, False if defect not found
            
        Raises:
            ValueError: If the transition is invalid
        """
        defect = self.get_defect(defect_id)
        if not defect:
            return False
        
        defect.change_status(new_status, changed_by, comment)
        return True
    
    def get_defects_by_status(self, status: DefectStatus) -> List[Defect]:
        """Get all defects with a specific status"""
        return [d for d in self.defects.values() if d.status == status]
    
    def get_all_defects(self) -> List[Defect]:
        """Get all defects"""
        return list(self.defects.values())
    
    def get_defects_by_priority(self, priority: DefectPriority) -> List[Defect]:
        """Get all defects with a specific priority"""
        return [d for d in self.defects.values() if d.priority == priority]
