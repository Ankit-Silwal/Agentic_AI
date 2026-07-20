from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
import json
import os
import requests
from typing import Optional, Any,Union
load_dotenv()
client = OpenAI(
    api_key=os.getenv("api_key"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd:str):
  result=os.system(cmd)
  return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"

def write_file(path:str,content:str):
  with open(path,"w") as f:
    f.write(content)

available_tools = {
    "get_weather": get_weather,
    "run_command":run_command,
    "write_file":write_file
}

SYSTEM_PROMPT = """
You are an expert AI assistant that uses a chain-of-thought workflow with three step types: START, PLAN, and OUTPUT.

Workflow rules:
- First reply with a single JSON object with "step": "START" describing your understanding of the user's request.
- After START, reply with one PLAN step at a time (each reply contains exactly one JSON object with "step": "PLAN"). You may return multiple PLAN steps in separate messages to show an incremental plan.
- Make the planning stage longer if the question is harder like really longer you may take it to 100-1000000 steps depending upon complexity take it minimum 10 for anything.
- When planning is complete, reply with a single JSON object with "step": "OUTPUT" containing the final answer or result.
- You can also call a tool if required from the list of available tools.
- For every tool call wait for the OBSERVE which is the output from the called tool.

Available Tools:
- get_weather(city:str): Takes city name as an input string and returns the weather information about the city.
-run_command(cmd:str): Takes a system linux command as string and executes the command on user's system and return the output from that command
-write_file(path:str,content:str):Path has the information about the path of the file and content has about the content that needs to be written down

Output Json Format:

START / PLAN / OUTPUT:
{"step":"START|PLAN|OUTPUT","content":"string"}

TOOL:
{"step":"TOOL","tool":"string","input":"string"}

OBSERVE:
{"step":"OBSERVE","tool":"string","input":"string","output":"string"}

Formatting rules:
- Every response must be a single valid JSON object and nothing else (no extra text).
- Return only one step per response.

Example interaction:

User: "Hey, can you solve 2+4*4?"

Assistant:
{"step":"START","content":"User asked to evaluate the arithmetic expression 2+4*4."}

Assistant:
{"step":"PLAN","content":"Apply operator precedence: multiply before addition."}

Assistant:
{"step":"PLAN","content":"Compute 4*4 = 16 then add 2."}

Assistant:
{"step":"OUTPUT","content":"18"}

User: "What is the weather of Delhi?"

Assistant:
{"step":"START","content":"Seems like you are interested in getting weather of Delhi."}

Assistant:
{"step":"PLAN","content":"Let's check available tools."}

Assistant:
{"step":"PLAN","content":"The get_weather tool is available."}

Assistant:
{"step":"PLAN","content":"Calling get_weather with Delhi."}

Assistant:
{"step":"TOOL","tool":"get_weather","input":"delhi"}

Assistant receives:
{"step":"OBSERVE","tool":"get_weather","input":"delhi","output":"The weather in delhi is Cloudy +20°C"}

Assistant:
{"step":"OUTPUT","content":"The current weather in Delhi is Cloudy +20°C."}
"""

print("\n\n\n")
class WriteFileInput(BaseModel):
    path: str
    content: str


class MyOutputFormat(BaseModel):
    step: str
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[Union[str, WriteFileInput]] = None


message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

user_query = input("Ask your question:")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.beta.chat.completions.parse(
        model="gemini-3.1-flash-lite",
        response_format=MyOutputFormat,
        messages=message_history
    )

    raw_result = response.choices[0].message.content

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "START":
        print("START->", parsed_result.content)
        continue
    if parsed_result.step == "TOOL":
        tool_to_call = parsed_result.tool
        tool_input = parsed_result.input
        print(parsed_result)
        print(type(parsed_result.input))
        print(parsed_result.input)

        if isinstance(tool_input, dict):
          tool_response = available_tools[tool_to_call](**tool_input)
        else:
          tool_response = available_tools[tool_to_call](tool_input)
        print(f"Tool->:{tool_to_call}({tool_input})={tool_response}")

        message_history.append({
            "role": "user",
            "content": json.dumps({
                "step": "OBSERVE",
                "tool": tool_to_call,
                "input": tool_input,
                "output": tool_response
            })
        })

        continue

    if parsed_result.step == "PLAN":
        print("Thinking..->", parsed_result.content)
        continue

    if parsed_result.step == "OUTPUT":
        print("Output->", parsed_result.content)
        break

print("\n\n\n")