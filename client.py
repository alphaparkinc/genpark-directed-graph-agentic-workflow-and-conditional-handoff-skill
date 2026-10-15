"""Directed Graph Agentic Workflow & Conditional Handoff Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional, Callable


class DirectedGraphWorkflow:
    """Orchestrates multi-agent execution using directed graphs with conditional edges,
    evaluating runtime state to route execution to appropriate subagents or completion nodes."""

    def __init__(self):
        # Maps node_id -> {"description": str, "agent_role": str}
        self.nodes: Dict[str, Dict[str, Any]] = {}
        # Maps (from_node, condition_val) -> to_node
        self.conditional_edges: Dict[str, List[Dict[str, Any]]] = {}

    def add_node(self, node_id: str, description: str = "", agent_role: str = "") -> Dict[str, Any]:
        """Registers an execution node in the workflow graph."""
        self.nodes[node_id] = {
            "node_id": node_id,
            "description": description,
            "agent_role": agent_role,
        }
        if node_id not in self.conditional_edges:
            self.conditional_edges[node_id] = []
        return {"status": "NODE_ADDED", "node_id": node_id}

    def add_conditional_edge(
        self,
        from_node: str,
        to_node: str,
        condition_key: str,
        expected_value: Any,
        description: str = "",
    ) -> Dict[str, Any]:
        """Adds a conditional branch from from_node to to_node when state[condition_key] == expected_value."""
        if from_node not in self.conditional_edges:
            self.conditional_edges[from_node] = []

        edge = {
            "to_node": to_node,
            "condition_key": condition_key,
            "expected_value": expected_value,
            "description": description,
        }
        self.conditional_edges[from_node].append(edge)
        return {"status": "EDGE_ADDED", "from_node": from_node, "to_node": to_node}

    def evaluate_next_step(self, current_node: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates outgoing conditional edges from current_node against the runtime state."""
        if current_node not in self.nodes:
            return {
                "error": f"Current node '{current_node}' is not registered in the workflow graph.",
                "next_node": None,
                "handoff": False,
            }

        outgoing = self.conditional_edges.get(current_node, [])
        for edge in outgoing:
            key = edge["condition_key"]
            expected = edge["expected_value"]
            if key in state and state[key] == expected:
                next_node_id = edge["to_node"]
                target_role = self.nodes.get(next_node_id, {}).get("agent_role", "")
                return {
                    "matched": True,
                    "from_node": current_node,
                    "next_node": next_node_id,
                    "agent_role": target_role,
                    "handoff_required": bool(target_role),
                    "reason": f"State condition '{key} == {expected}' matched edge to '{next_node_id}'.",
                }

        # Fallback or completion
        return {
            "matched": False,
            "from_node": current_node,
            "next_node": None,
            "handoff_required": False,
            "status": "TERMINATED_OR_NO_MATCH",
            "message": f"No outgoing conditional edge from '{current_node}' matched the current state.",
        }

    def get_topology(self) -> Dict[str, Any]:
        """Returns the full graph representation for debugging or Mermaid rendering."""
        return {
            "node_count": len(self.nodes),
            "nodes": list(self.nodes.values()),
            "edges": self.conditional_edges,
        }
