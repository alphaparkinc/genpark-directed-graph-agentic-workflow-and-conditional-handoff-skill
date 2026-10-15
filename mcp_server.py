"""MCP server for Directed Graph Agentic Workflow & Conditional Handoff."""
import sys
import json
from client import DirectedGraphWorkflow

_workflow = DirectedGraphWorkflow()


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "add_workflow_node",
                    "description": "Registers an agent execution node or subagent worker in the workflow graph",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "node_id": {"type": "string"},
                            "description": {"type": "string", "default": ""},
                            "agent_role": {"type": "string", "default": ""},
                        },
                        "required": ["node_id"],
                    },
                },
                {
                    "name": "add_conditional_edge",
                    "description": "Defines a state transition condition from one agent node to another",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "from_node": {"type": "string"},
                            "to_node": {"type": "string"},
                            "condition_key": {"type": "string"},
                            "expected_value": {},
                        },
                        "required": ["from_node", "to_node", "condition_key", "expected_value"],
                    },
                },
                {
                    "name": "evaluate_next_step",
                    "description": "Evaluates current agent state to determine the next branch and agent handoff",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "current_node": {"type": "string"},
                            "state": {"type": "object"},
                        },
                        "required": ["current_node", "state"],
                    },
                },
                {
                    "name": "get_workflow_topology",
                    "description": "Returns full graph nodes and conditional edge structure",
                    "inputSchema": {"type": "object", "properties": {}},
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "add_workflow_node":
            res = _workflow.add_node(
                args.get("node_id", ""),
                description=args.get("description", ""),
                agent_role=args.get("agent_role", ""),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "add_conditional_edge":
            res = _workflow.add_conditional_edge(
                args.get("from_node", ""),
                args.get("to_node", ""),
                args.get("condition_key", ""),
                args.get("expected_value"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "evaluate_next_step":
            res = _workflow.evaluate_next_step(
                args.get("current_node", ""),
                args.get("state", {}),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "get_workflow_topology":
            res = _workflow.get_topology()
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
