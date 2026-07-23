import os
import json
from dotenv import load_dotenv
from google import genai
from mem0 import Memory

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=GEMINI_KEY)

config = {
    "version": "v1.1",
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_KEY,
            "model": "gemini-3.1-flash-lite"
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "Orange/orange-nomic-v1.5-1536"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

memory = Memory.from_config(config)

chat = client.chats.create(
    model="gemini-3.1-flash-lite"
)

while True:
    user_query = input("You: ")

    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    search_memory = memory.search(
        query=user_query,
        filters={
        "user_id": "ankitsilwal"
        }
    )

    memories = [
        f"Id: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory
    ]

    SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Here are the relevant memories about the user:

{json.dumps(memories, indent=2)}

Use these memories only if they are relevant to answering the user's message.
"""

    print("Found memories:", memories)

    response = chat.send_message(
        f"{SYSTEM_PROMPT}\n\nUser: {user_query}"
    )

    ai_response = response.text

    print("Assistant:", ai_response)

    memory.add(
        user_id="ankitsilwal",
        messages=[
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "assistant",
                "content": ai_response
            }
        ]
    )

    print("Memory saved.")