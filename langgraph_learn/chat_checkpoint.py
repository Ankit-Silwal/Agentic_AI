from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai",
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state["messages"])
    print("Inside chatbot node:", state)
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


DB_URI = "mongodb://admin:admin@localhost:27018"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = compile_graph_with_checkpointer(checkpointer)

    config = {
        "configurable": {
            "thread_id": "ankit"
        }
    }

    state = {
        "messages": [
            HumanMessage(content="What is my name")
        ]
    }

    updated_state = graph.invoke(state, config=config)

    print("\nUpdated State:")
    print(updated_state)