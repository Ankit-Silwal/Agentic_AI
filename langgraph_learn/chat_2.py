from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("api_key"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[
            {"role": "user", "content": state["user_query"]}
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    """
    Dummy evaluation logic.
    Change this however you want.
    """

    if "2+2" in state["user_query"]:
        return "endnode"

    return "chatbot_gemini"


def chatbot_gemini(state: State):
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[
            {"role": "user", "content": state["user_query"]}
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def endnode(state: State):
    return state



graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response,
)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()


updated_state = graph.invoke(
    {
        "user_query": "Hey, what is 2+2?"
    }
)

print(updated_state)