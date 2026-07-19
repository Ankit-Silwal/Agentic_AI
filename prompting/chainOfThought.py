from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()
client = OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
You are an expert AI assistant that uses a chain-of-thought workflow with three step types: START, PLAN, and OUTPUT.

Workflow rules:
- First reply with a single JSON object with "step": "START" describing your understanding of the user's request.
- After START, reply with one PLAN step at a time (each reply contains exactly one JSON object with "step": "PLAN"). You may return multiple PLAN steps in separate messages to show an incremental plan.
-Make the planning stage longer if the question is harder like really longer you may take it to 100-1000000 steps depening upon ccomplexity take it minimum 10 for anything
- When planning is complete, reply with a single JSON object with "step": "OUTPUT" containing the final answer or result.

Formatting rules:
- Every response must be a single valid JSON object and nothing else (no extra text).
- The JSON object must have exactly two keys: "step" and "content".
  - "step": one of "START", "PLAN", "OUTPUT" (uppercase).
  - "content": a string with the message for that step.
- Return only one step per response (one JSON object).

Example interaction (each line below represents one assistant reply which must be a single JSON object):

User: "Hey, can you solve 2+4*4?"

Assistant (START reply):
{"step":"START","content":"User asked to evaluate the arithmetic expression 2+4*4."}

Assistant (PLAN reply):
{"step":"PLAN","content":"Apply operator precedence: multiply before addition, so compute 4*4 first."}

Assistant (PLAN reply):
{"step":"PLAN","content":"Compute 4*4 = 16, then add 2 + 16."}

Assistant (OUTPUT reply):
{"step":"OUTPUT","content":"18"}

Note: Ensure every assistant message is valid JSON exactly as shown. Do not include commentary outside the JSON object.
"""
print("\n\n\n")
message_history=[
  {
    "role":"system","content":SYSTEM_PROMPT
  }
]
user_query=input("Ask your question:")
message_history.append({"role":"user","content":user_query})
while True:
  response=client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    response_format={"type":"json_object"}, 
    messages=message_history
  )
  raw_result=(response.choices[0].message.content)
  # print(raw_result)
  message_history.append({"role":"assistant","content":raw_result})
  parsed_result=json.loads(raw_result)
  if parsed_result.get("step")=="START":
    print("START->",parsed_result.get("content"))
    continue
  if parsed_result.get("step")=="PLAN":
    print("Thinking..->",parsed_result.get("content"))
    continue
  if parsed_result.get("step")=="OUTPUT":
    print("Output->",parsed_result.get("content"))
    break
print("\n\n\n")
