from agents import planner_node, researcher_node, writer_node, reviewer_node

state = {"topic": "The Impact of AI on Employment"}
state.update(planner_node(state))
state.update(researcher_node(state))
state.update(writer_node(state))
state.update(reviewer_node(state))

print("\n--- Verdict ---")
print("Approuved :", state["approved"])
print("Revisions :", state["revision_count"])
print("\n--- Reviewer's comments ---\n")
print(state["review"][:800])