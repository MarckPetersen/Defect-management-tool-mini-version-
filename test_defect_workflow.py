"""
Unit tests for the Defect Status Workflow Management System
"""

import unittest
from defect_workflow import (
    Defect, DefectManager, DefectStatus, DefectPriority, 
    DefectWorkflow, StatusChange
)


class TestDefectWorkflow(unittest.TestCase):
    """Test cases for DefectWorkflow class"""
    
    def test_valid_transitions_from_new(self):
        """Test valid transitions from NEW status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.NEW, DefectStatus.IN_PROGRESS))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.NEW, DefectStatus.CLOSED))
    
    def test_invalid_transitions_from_new(self):
        """Test invalid transitions from NEW status"""
        self.assertFalse(DefectWorkflow.is_valid_transition(
            DefectStatus.NEW, DefectStatus.TESTING))
        self.assertFalse(DefectWorkflow.is_valid_transition(
            DefectStatus.NEW, DefectStatus.RESOLVED))
        self.assertFalse(DefectWorkflow.is_valid_transition(
            DefectStatus.NEW, DefectStatus.REOPENED))
    
    def test_valid_transitions_from_in_progress(self):
        """Test valid transitions from IN_PROGRESS status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.IN_PROGRESS, DefectStatus.TESTING))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.IN_PROGRESS, DefectStatus.NEW))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.IN_PROGRESS, DefectStatus.CLOSED))
    
    def test_valid_transitions_from_testing(self):
        """Test valid transitions from TESTING status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.TESTING, DefectStatus.RESOLVED))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.TESTING, DefectStatus.IN_PROGRESS))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.TESTING, DefectStatus.REOPENED))
    
    def test_valid_transitions_from_resolved(self):
        """Test valid transitions from RESOLVED status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.RESOLVED, DefectStatus.CLOSED))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.RESOLVED, DefectStatus.REOPENED))
    
    def test_valid_transitions_from_closed(self):
        """Test valid transitions from CLOSED status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.CLOSED, DefectStatus.REOPENED))
    
    def test_valid_transitions_from_reopened(self):
        """Test valid transitions from REOPENED status"""
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.REOPENED, DefectStatus.IN_PROGRESS))
        self.assertTrue(DefectWorkflow.is_valid_transition(
            DefectStatus.REOPENED, DefectStatus.CLOSED))
    
    def test_get_allowed_transitions(self):
        """Test getting allowed transitions for a status"""
        allowed = DefectWorkflow.get_allowed_transitions(DefectStatus.NEW)
        self.assertEqual(len(allowed), 2)
        self.assertIn(DefectStatus.IN_PROGRESS, allowed)
        self.assertIn(DefectStatus.CLOSED, allowed)


class TestDefect(unittest.TestCase):
    """Test cases for Defect class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Reset the ID counter for consistent testing
        Defect._id_counter = 1
    
    def test_defect_creation(self):
        """Test creating a new defect"""
        defect = Defect(
            title="Login button not working",
            description="Users cannot login",
            priority=DefectPriority.HIGH,
            created_by="john@example.com"
        )
        
        self.assertEqual(defect.title, "Login button not working")
        self.assertEqual(defect.description, "Users cannot login")
        self.assertEqual(defect.priority, DefectPriority.HIGH)
        self.assertEqual(defect.status, DefectStatus.NEW)
        self.assertEqual(defect.created_by, "john@example.com")
        self.assertIsNotNone(defect.created_at)
        self.assertIsNone(defect.assigned_to)
    
    def test_valid_status_change(self):
        """Test valid status change"""
        defect = Defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.MEDIUM,
            created_by="test@example.com"
        )
        
        result = defect.change_status(
            DefectStatus.IN_PROGRESS,
            changed_by="dev@example.com",
            comment="Starting work on this"
        )
        
        self.assertTrue(result)
        self.assertEqual(defect.status, DefectStatus.IN_PROGRESS)
        self.assertEqual(len(defect.status_history), 1)
        
        history = defect.status_history[0]
        self.assertEqual(history.from_status, DefectStatus.NEW)
        self.assertEqual(history.to_status, DefectStatus.IN_PROGRESS)
        self.assertEqual(history.changed_by, "dev@example.com")
        self.assertEqual(history.comment, "Starting work on this")
    
    def test_invalid_status_change(self):
        """Test invalid status change raises ValueError"""
        defect = Defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.LOW,
            created_by="test@example.com"
        )
        
        with self.assertRaises(ValueError) as context:
            defect.change_status(
                DefectStatus.RESOLVED,
                changed_by="dev@example.com"
            )
        
        self.assertIn("Invalid transition", str(context.exception))
        self.assertEqual(defect.status, DefectStatus.NEW)
    
    def test_multiple_status_changes(self):
        """Test multiple status changes maintain history"""
        defect = Defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.CRITICAL,
            created_by="test@example.com"
        )
        
        # NEW -> IN_PROGRESS
        defect.change_status(DefectStatus.IN_PROGRESS, "dev1@example.com", "Starting")
        # IN_PROGRESS -> TESTING
        defect.change_status(DefectStatus.TESTING, "dev1@example.com", "Ready for testing")
        # TESTING -> RESOLVED
        defect.change_status(DefectStatus.RESOLVED, "tester@example.com", "Tests passed")
        
        self.assertEqual(defect.status, DefectStatus.RESOLVED)
        self.assertEqual(len(defect.status_history), 3)
        
        # Verify history order
        self.assertEqual(defect.status_history[0].to_status, DefectStatus.IN_PROGRESS)
        self.assertEqual(defect.status_history[1].to_status, DefectStatus.TESTING)
        self.assertEqual(defect.status_history[2].to_status, DefectStatus.RESOLVED)
    
    def test_assign_to(self):
        """Test assigning defect to a user"""
        defect = Defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.MEDIUM,
            created_by="test@example.com"
        )
        
        defect.assign_to("dev@example.com")
        self.assertEqual(defect.assigned_to, "dev@example.com")
    
    def test_get_status_history(self):
        """Test getting status history returns a copy"""
        defect = Defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.LOW,
            created_by="test@example.com"
        )
        
        defect.change_status(DefectStatus.IN_PROGRESS, "dev@example.com")
        
        history1 = defect.get_status_history()
        history2 = defect.get_status_history()
        
        # Should be equal but not the same object
        self.assertEqual(len(history1), len(history2))
        self.assertIsNot(history1, history2)


class TestDefectManager(unittest.TestCase):
    """Test cases for DefectManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        Defect._id_counter = 1
        self.manager = DefectManager()
    
    def test_create_defect(self):
        """Test creating a defect through the manager"""
        defect = self.manager.create_defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.HIGH,
            created_by="test@example.com"
        )
        
        self.assertIsNotNone(defect)
        self.assertEqual(defect.id, 1)
        self.assertEqual(defect.title, "Test defect")
        self.assertEqual(len(self.manager.defects), 1)
    
    def test_get_defect(self):
        """Test retrieving a defect by ID"""
        defect = self.manager.create_defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.MEDIUM,
            created_by="test@example.com"
        )
        
        retrieved = self.manager.get_defect(defect.id)
        self.assertEqual(retrieved, defect)
        
        # Test non-existent defect
        self.assertIsNone(self.manager.get_defect(999))
    
    def test_update_defect_status(self):
        """Test updating defect status through the manager"""
        defect = self.manager.create_defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.LOW,
            created_by="test@example.com"
        )
        
        result = self.manager.update_defect_status(
            defect.id,
            DefectStatus.IN_PROGRESS,
            "dev@example.com",
            "Starting work"
        )
        
        self.assertTrue(result)
        self.assertEqual(defect.status, DefectStatus.IN_PROGRESS)
    
    def test_update_defect_status_invalid_id(self):
        """Test updating status for non-existent defect"""
        result = self.manager.update_defect_status(
            999,
            DefectStatus.IN_PROGRESS,
            "dev@example.com"
        )
        
        self.assertFalse(result)
    
    def test_update_defect_status_invalid_transition(self):
        """Test updating status with invalid transition"""
        defect = self.manager.create_defect(
            title="Test defect",
            description="Test description",
            priority=DefectPriority.HIGH,
            created_by="test@example.com"
        )
        
        with self.assertRaises(ValueError):
            self.manager.update_defect_status(
                defect.id,
                DefectStatus.RESOLVED,
                "dev@example.com"
            )
    
    def test_get_defects_by_status(self):
        """Test filtering defects by status"""
        # Create multiple defects
        d1 = self.manager.create_defect("Defect 1", "Desc 1", DefectPriority.HIGH, "user1")
        d2 = self.manager.create_defect("Defect 2", "Desc 2", DefectPriority.MEDIUM, "user2")
        d3 = self.manager.create_defect("Defect 3", "Desc 3", DefectPriority.LOW, "user3")
        
        # Change some statuses
        d1.change_status(DefectStatus.IN_PROGRESS, "dev1")
        d2.change_status(DefectStatus.IN_PROGRESS, "dev2")
        
        # Get defects by status
        new_defects = self.manager.get_defects_by_status(DefectStatus.NEW)
        in_progress_defects = self.manager.get_defects_by_status(DefectStatus.IN_PROGRESS)
        
        self.assertEqual(len(new_defects), 1)
        self.assertEqual(len(in_progress_defects), 2)
        self.assertIn(d3, new_defects)
        self.assertIn(d1, in_progress_defects)
        self.assertIn(d2, in_progress_defects)
    
    def test_get_all_defects(self):
        """Test getting all defects"""
        self.manager.create_defect("Defect 1", "Desc 1", DefectPriority.HIGH, "user1")
        self.manager.create_defect("Defect 2", "Desc 2", DefectPriority.MEDIUM, "user2")
        self.manager.create_defect("Defect 3", "Desc 3", DefectPriority.LOW, "user3")
        
        all_defects = self.manager.get_all_defects()
        self.assertEqual(len(all_defects), 3)
    
    def test_get_defects_by_priority(self):
        """Test filtering defects by priority"""
        d1 = self.manager.create_defect("Defect 1", "Desc 1", DefectPriority.HIGH, "user1")
        d2 = self.manager.create_defect("Defect 2", "Desc 2", DefectPriority.HIGH, "user2")
        d3 = self.manager.create_defect("Defect 3", "Desc 3", DefectPriority.LOW, "user3")
        
        high_priority = self.manager.get_defects_by_priority(DefectPriority.HIGH)
        low_priority = self.manager.get_defects_by_priority(DefectPriority.LOW)
        
        self.assertEqual(len(high_priority), 2)
        self.assertEqual(len(low_priority), 1)
        self.assertIn(d1, high_priority)
        self.assertIn(d2, high_priority)
        self.assertIn(d3, low_priority)


class TestStatusChange(unittest.TestCase):
    """Test cases for StatusChange class"""
    
    def test_status_change_creation(self):
        """Test creating a status change record"""
        change = StatusChange(
            from_status=DefectStatus.NEW,
            to_status=DefectStatus.IN_PROGRESS,
            changed_by="dev@example.com",
            comment="Starting work"
        )
        
        self.assertEqual(change.from_status, DefectStatus.NEW)
        self.assertEqual(change.to_status, DefectStatus.IN_PROGRESS)
        self.assertEqual(change.changed_by, "dev@example.com")
        self.assertEqual(change.comment, "Starting work")
        self.assertIsNotNone(change.timestamp)


if __name__ == '__main__':
    unittest.main()
