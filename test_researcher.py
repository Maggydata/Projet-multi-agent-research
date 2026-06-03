from agents import planner_node, researcher_node

state = {"topic": "The Impact of AI on Employment"}

state.update(planner_node(state))
state.update(researcher_node(state))

print("\n--- Overview of the first research block ---")
print(state["research"][0][:500])