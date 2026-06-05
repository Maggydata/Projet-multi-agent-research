from config import llm, search_tool
from state import ResearchState



def planner_node(state: ResearchState) -> dict:
    """Transform the topic into a list of research questions."""
    topic = state["topic"]

    # The LLM generate output in simple, easy-to-parse lines.
    prompt = f"""You are a research planner.
Topic : "{topic}"

Generate between 3 and 5 precise and complementary research questions
that will allow you to cover this topic in depth.

Respond ONLY with the questions, one per line, without numbering,
without a hyphen or introductory text."""

    response = llm.invoke(prompt)

    # We remove the spaces and ignore the blank lines.
    plan = [
        line.strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    print(f"Planner : {len(plan)} questions generated")
    for q in plan:
        print(f"   - {q}")

    # We return ONLY the field we are updating.
    return {"plan": plan}


def researcher_node(state: ResearchState) -> dict:
    """For each question in the plan, perform a web search using Tavily."""
    plan = state["plan"]
    collected = []

    for question in plan:
        print(f"🔎 Researcher : searching → {question}")

        # search_tool.invoke expects a dictionary with the key "query".
        result = search_tool.invoke({"query": question})

        # format one readable block per question.
        sources = result.get("results", [])
        block = f"### Question : {question}\n"
        for s in sources:
            title = s.get("title", "Sans titre")
            url = s.get("url", "")
            content = s.get("content", "")
            block += f"\n**{title}** ({url})\n{content}\n"

        collected.append(block)

    print(f"Researcher : {len(collected)} collected search queries")

    return {"research": collected}


def writer_node(state: ResearchState) -> dict:
    """Write a structured report based on the collected research."""
    topic = state["topic"]
    research = state["research"]

    # If there's already a review, we'll forward it
    review = state.get("review", "")

    # We combine all the search blocks into a single source text.
    research_text = "\n\n".join(research)

    # Correction instructions are added only if there is reviewer feedback.
    revision_instruction = ""
    if review:
        revision_instruction = f"""
A reviewer made the following comments on your previous version.
Please revise the report accordingly :
{review}
"""

    prompt = f"""You are a research report writer.
Topic : "{topic}"

Here are the collected research results :
{research_text}
{revision_instruction}

Write a clear and structured report in French, with :
- an introduction,
- sections with subtitles,
- a conclusion.

Rely solely on the information provided above."""

    response = llm.invoke(prompt)
    draft = response.content

    print(f" Writer : report written ({len(draft)} characters)")

    return {"draft": draft}

def reviewer_node(state: ResearchState) -> dict:
    """Evaluate the draft : approved or to be revised, with comments."""
    topic = state["topic"]
    draft = state["draft"]

    # Revision counter : we read the existing
    revision_count = state.get("revision_count", 0) + 1

    prompt = f"""You are a demanding reviewer of research reports.
Topic : "{topic}"

Here is the report to evaluate :
{draft}

Evaluate the quality, structure and completeness of the report.

Start your answer with EXACTLY one of these two words, on its own on the first line:
APPROUVED
or
TO_BE_REVIEWED

Then, on the following lines, justify your evaluation with some concrete points.
If you write TO_BE_REVIEWED, provide specific correction instructions."""

    response = llm.invoke(prompt)
    content = response.content

    # The verdict is right there in the first line.
    first_line = content.split("\n")[0].strip().upper()
    approved = first_line.startswith("APPROUVED")

    print(f" Reviewer : {'APPROUVED ' if approved else 'TO BE REVIEWED '} "
          f"(revision n°{revision_count})")

    return {
        "review": content,
        "approved": approved,
        "revision_count": revision_count,
    }