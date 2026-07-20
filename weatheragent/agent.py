from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests

load_dotenv()
client = OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
def get_weather(city:str):
  url=f"https://wttr.in/{city.lower()}?format=%C+%t"
  response=requests.get(url)
  
  if(response.status_code==200):
    return f"The weather in {city} is {response.text}"
  
  return "Something went wrong"

available_tools={
  "get_weather":get_weather
}

SYSTEM_PROMPT = """
You are an expert AI assistant that uses a chain-of-thought workflow with three step types: START, PLAN, and OUTPUT.

Workflow rules:
- First reply with a single JSON object with "step": "START" describing your understanding of the user's request.
- After START, reply with one PLAN step at a time (each reply contains exactly one JSON object with "step": "PLAN"). You may return multiple PLAN steps in separate messages to show an incremental plan.
-Make the planning stage longer if the question is harder like really longer you may take it to 100-1000000 steps depening upon ccomplexity take it minimum 10 for anything
- When planning is complete, reply with a single JSON object with "step": "OUTPUT" containing the final answer or result.
-You can also call a tool if required from the list of available tools
-for every tool call wait for the observe which is the output from the called tool.
Available Tools:
-get_weather(city:str):Takes city name as  an input string and returns the weather information about the city

Output Json Format:
{"step":"START"|"PLAN"|"OUTPUT"|"TOOL","content":"string","tool":"string","input":"string","output":"string"}
Formatting rules:
- Every response must be a single valid JSON object and nothing else (no extra text).
- The JSON object must have exactly two keys: "step" and "content".
  - "step": one of "START", "PLAN", "OUTPUT","TOOL" (uppercase).
  - "content": a string with the message for that step.
- Return only one step per response (one JSON object).

Example interaction (each line below represents one assistant reply which must be a single JSON object):
Example 1:
User: "Hey, can you solve 2+4*4?"

Assistant (START reply):
{"step":"START","content":"User asked to evaluate the arithmetic expression 2+4*4."}

Assistant (PLAN reply):
{"step":"PLAN","content":"Apply operator precedence: multiply before addition, so compute 4*4 first."}

Assistant (PLAN reply):
{"step":"PLAN","content":"Compute 4*4 = 16, then add 2 + 16."}

Assistant (OUTPUT reply):
{"step":"OUTPUT","content":"18"}

Example 2:
User: "WHat is the weather of Delhi?"

Assistant (START reply):
{"step":"START","content":"Seems like you are interested in getting weather of delhi in India."}

Assistant (PLAN reply):
{"step":"PLAN","content":"Lets see if we have any available tools from the list of available tools"}

Assistant (PLAN reply):
{"step":"PLAN","content":"Great,we have get_weather tool available for this query"}

Assistant (PLAN reply):
{"step":"PLAN","content":"I need to call get_weather tool for delhi and input for city"}

Assistant (TOOL reply):
{"step":"PLAN","tool":"get_weather",input":"delhi"}

Assistant (OBSERVE reply):
{"step":"OBSERVE","tool":"get_weather",output":"The temperature of delhi is cloudy with 20 d celcius"}

Assistant (OUTPUT reply):
{"step":"OUTPUT","content":"Great,I got the weather info about delhi"}


Assistant (OUTPUT reply):
{"step":"OUTPUT","content":"The current temperature in delhi is 20 C with come cloudy sky."}

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
  
  if parsed_result.get("step")=="TOOL":
    tool_to_call=parsed_result.get("tool")
    tool_input=parsed_result.get("input")
    
    tool_response=available_tools[tool_to_call](tool_input)
    print(f"Tool->:{tool_to_call}({tool_input})={tool_response}")
    message_history.append({"role":"developer","content":json.dumps({
      "step":"OBSERVE","tool":tool_to_call,"input":tool_input,"output":tool_response
    })})
    continue
    
    
  if parsed_result.get("step")=="PLAN":
    print("Thinking..->",parsed_result.get("content"))
    continue
  if parsed_result.get("step")=="OUTPUT":
    print("Output->",parsed_result.get("content"))
    break
print("\n\n\n")
