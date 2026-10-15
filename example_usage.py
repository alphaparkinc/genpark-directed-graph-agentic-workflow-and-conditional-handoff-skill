"""Example usage for Directed Graph Agentic Workflow & Conditional Handoff."""
from client import DirectedGraphWorkflow

if __name__ == "__main__":
    wf = DirectedGraphWorkflow()

    # 1. Define nodes
    wf.add_node("code_generator", description="Generates initial Python feature code", agent_role="Developer")
    wf.add_node("unit_tester", description="Executes pytest suite", agent_role="QA Engineer")
    wf.add_node("bug_fixer", description="Fixes failed assertions", agent_role="Debugger")
    wf.add_node("pr_creator", description="Opens pull request", agent_role="Release Manager")

    # 2. Add conditional transitions
    wf.add_conditional_edge("unit_tester", "pr_creator", condition_key="tests_passed", expected_value=True)
    wf.add_conditional_edge("unit_tester", "bug_fixer", condition_key="tests_passed", expected_value=False)

    # 3. Simulate runtime state evaluation: test failure
    failed_state = {"tests_passed": False, "failed_count": 2}
    res_fail = wf.evaluate_next_step("unit_tester", failed_state)
    print("Test Failure Handoff:")
    print("  Next Node:", res_fail["next_node"])
    print("  Agent Role:", res_fail["agent_role"])
    print("  Reason:", res_fail["reason"])

    # 4. Simulate runtime state evaluation: test success
    pass_state = {"tests_passed": True, "failed_count": 0}
    res_pass = wf.evaluate_next_step("unit_tester", pass_state)
    print("\nTest Success Handoff:")
    print("  Next Node:", res_pass["next_node"])
    print("  Agent Role:", res_pass["agent_role"])
    print("  Reason:", res_pass["reason"])
