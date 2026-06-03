from langgraph.graph import StateGraph, START, END
from state import ResearchState
from agents import planner_node, researcher_node, writer_node, reviewer_node

# Maximum number of writer-reviewer cycles
MAX_REVISIONS = 2


def route_after_review(state: ResearchState) -> str:
    """Function for routing : decides where to go AFTER the reviewer.
    Returns a STRING that will be mapped to a node (or END)."""
    if state["approved"]:
        return "approved"
    if state["revision_count"] >= MAX_REVISIONS:
        # We have reached the limit : we stop even if not approved.
        print(f"Limit of {MAX_REVISIONS} revisions reached, we finish.")
        return "approved"
    
    return "revise"


def build_graph():
    # Creating the graph
    builder = StateGraph(ResearchState)

    # Recording of each node
    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("writer", writer_node)
    builder.add_node("reviewer", reviewer_node)

    # Outgoing flow
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")

    #the dictionary maps these strings to destinations.
    builder.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "approved": END,       # fin du graphe
            "revise": "writer",    # boucle : retour au writer
        },
    )

    return builder.compile()