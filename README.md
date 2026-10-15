# genpark-directed-graph-agentic-workflow-and-conditional-handoff-skill

Orchestrates multi-agent execution graphs with state-evaluated conditional edges, dynamic routing, and subagent handoffs.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Directed Graph Routing**: Models non-linear agent reasoning loops, fallback branches, and sequential steps as a state machine.
- **Dynamic Conditional Handoff**: Inspects real-time trajectory state (e.g., test outcomes, validation scores, approval flags) to transition control to the designated specialist subagent.
- **Role & Intent Assignment**: Binds explicit agent personas (e.g., Developer, QA Engineer, Debugger, Release Manager) to graph nodes for automated delegation.
- **Topology Introspection**: Exports the complete workflow graph for visual debugging or runtime observability.

## Architecture

```
[Agent Output / Execution State]
               │
               ▼
┌──────────────────────────────────────────────┐
│        DirectedGraphWorkflow Engine          │
│  - Node Registry & Agent Roles               │
│  - Edge Evaluator (key == expected_value)    │
└──────────────────────────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
[Branch Match]     [Fallback / Complete]
  - Next Node        - Terminal State
  - Subagent Role    - Reason Log
  - Handoff Trigger
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `add_workflow_node`: Registers an agent execution node or subagent worker in the workflow graph.
- `add_conditional_edge`: Defines a state transition condition from one agent node to another.
- `evaluate_next_step`: Evaluates current agent state to determine the next branch and agent handoff.
- `get_workflow_topology`: Returns full graph nodes and conditional edge structure.

## Quickstart (Python API)

```python
from client import DirectedGraphWorkflow

wf = DirectedGraphWorkflow()

# 1. Define nodes with roles
wf.add_node("code_generator", description="Generates code", agent_role="Developer")
wf.add_node("unit_tester", description="Runs tests", agent_role="QA Engineer")
wf.add_node("bug_fixer", description="Fixes failed tests", agent_role="Debugger")

# 2. Add conditional transitions
wf.add_conditional_edge("unit_tester", "bug_fixer", condition_key="tests_passed", expected_value=False)

# 3. Evaluate state
next_step = wf.evaluate_next_step("unit_tester", {"tests_passed": False})
print("Handoff target:", next_step["next_node"], "Role:", next_step["agent_role"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
