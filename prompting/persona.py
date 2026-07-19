import json
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
client=OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
name=input("Who is talking :")
SYSTEM_PROMPT="""
Rules:
-Every response must be a single valid JSON object and nothing else
-Always follow the pattern example and take content from way of my talking
Example:
put some example too
1.{"type":"INPUT","user":"Anish","content":hello}
like this
You are acting on the behalf of Ankit Silwal who is 20 years old .
Way of my talking:


Put your chat in here export from the whatsapp


"""
message_history=[{
  "role":"system","content":SYSTEM_PROMPT
}]

while True:
  question=input()
  message_history.append({"role":"user","content":question})
  response=client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    response_format={"type":"json_object"},
    messages=message_history
  )
  raw_result=(response.choices[0].message.content)
  message_history.append({"role":"assistant","content":raw_result})
  parsed_result=json.loads(raw_result)
  
  if(parsed_result.get("type")=="OUTPUT"):
    print("Ankit->",parsed_result.get("content"))
    continue