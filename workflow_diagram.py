"""
Generate a visual representation of the defect workflow
"""

from defect_workflow import DefectStatus, DefectWorkflow


def generate_workflow_diagram():
    """Generate a text-based workflow diagram"""
    
    print("=" * 70)
    print("DEFECT STATUS WORKFLOW DIAGRAM")
    print("=" * 70)
    print()
    print("States and their allowed transitions:")
    print()
    
    for status in DefectStatus:
        allowed = DefectWorkflow.get_allowed_transitions(status)
        print(f"📌 {status.value}")
        if allowed:
            for target in allowed:
                print(f"   └─> {target.value}")
        else:
            print(f"   └─> (No outgoing transitions)")
        print()
    
    print()
    print("=" * 70)
    print("TYPICAL WORKFLOW PATH")
    print("=" * 70)
    print()
    print("Happy Path (No Issues):")
    print("  NEW ──> IN_PROGRESS ──> TESTING ──> RESOLVED ──> CLOSED")
    print()
    print("Path with Regression:")
    print("  NEW ──> IN_PROGRESS ──> TESTING ──> RESOLVED ──> CLOSED")
    print("                                                      │")
    print("                                                      v")
    print("                                                  REOPENED")
    print("                                                      │")
    print("                                                      v")
    print("                                              IN_PROGRESS (cycle)")
    print()
    print("Path with Failed Testing:")
    print("  NEW ──> IN_PROGRESS ──> TESTING")
    print("                            │")
    print("                            v")
    print("                        IN_PROGRESS (cycle)")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    generate_workflow_diagram()
