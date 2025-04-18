from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict, Any

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants

def rewrite(state: AgentState) -> Dict[str, Any]:
    messages = state["messages"]
    question = messages[0].content
    rewrite_count = state.get("rewrite_count", 0)

    # Max rewrite attempts to prevent looping
    MAX_REWRITE_ATTEMPTS = 2
    if rewrite_count >= MAX_REWRITE_ATTEMPTS:
        return {"messages": messages, "rewrite_count": rewrite_count}

    strategy = "Make the question more specific" if rewrite_count == 0 else "Broaden search scope"

    msg = [
        HumanMessage(
            content=f"""Transform this question for better results.
            Original question: {question}
            Strategy: {strategy}
            Provide only the rewritten question, no explanations."""
        )
    ]

    model = ChatOpenAI(temperature=0, model=constants.LLM_MODEL, streaming=True)
    response = model.invoke(msg)

    return {
        "messages": [response],
        "rewrite_count": rewrite_count + 1
    }
