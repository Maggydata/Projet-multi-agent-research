import sys
from datetime import datetime
from graph import build_graph


def save_report(topic: str, final_state: dict) -> str:
    """Writes the report to a timestamped Markdown file."""
    # replace the problematic characters in the subject line
    safe_topic = "".join(
        c if c.isalnum() or c in " -_" else "_" for c in topic
    ).strip().replace(" ", "_")[:50]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{safe_topic}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Report : {topic}\n\n")
        f.write(f"_Generated on {datetime.now().strftime('%d/%m/%Y at %H:%M')}_\n\n")
        f.write(f"_Status : {'Approved' if final_state['approved'] else 'Not approved'} "
                f"after {final_state['revision_count']} revision(s)_\n\n")
        f.write("---\n\n")
        f.write(final_state["draft"])

    return filename


def run(topic: str):
    graph = build_graph()

    initial_state = {
        "topic": topic,
        "research": [],
        "revision_count": 0,
    }

    print(f"\n Launching the graph on the topic : « {topic} »\n")

    # Error handling : we catch the errors (API, network, parsing)
    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        print(f"\n An error occurred during execution : {e}")
        print("Please check your API keys, quota, and connection.")
        return None

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60 + "\n")
    print(final_state["draft"])

    # Save to disk.
    filename = save_report(topic, final_state)
    print("\n" + "=" * 60)
    print(f" Report saved to : {filename}")
    print(f"Approved : {final_state['approved']} | "
          f"Revisions : {final_state['revision_count']}")
    print("=" * 60)

    return final_state


if __name__ == "__main__":
    # If a topic is passed as an argument, we use it ;
    # otherwise we ask the user, otherwise default value.
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Topic of the report : ").strip()
        if not topic:
            topic = "The Impact of AI on Employment"

    run(topic)