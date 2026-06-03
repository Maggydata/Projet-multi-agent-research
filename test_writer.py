from agents import planner_node, researcher_node, writer_node

state = {"topic": "The Impact of AI on Employment"}
state.update(planner_node(state))
state.update(researcher_node(state))
state.update(writer_node(state))

print("\n--- Beginning of the report ---\n")
print(state["draft"][:1000])