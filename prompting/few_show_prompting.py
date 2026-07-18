from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
question=input("Enter your question:")
#Few shot prompting
# In here we give some prompt with examples what happens in what condition and so ona ll the shits this is known as few sort prompting
SYSTEM_PROMPT = """Your job is to only answer coding related problems do not answer anything else your name is gubbinlubbin you are a bot for a code helper company
If user asks anything else just say sorry and tell about yourself who are you why are you
Rule:
-Strictly follow the output in json format
Outfut Format:
{
{
  "code:"string" or null,
  "isCodingQuestion":boolean,
  "error":error reason or null
}
}
Examples:
Q:Can you explain the a+b whole square
A:Sorry ,I can only help with coding related questions

Q:Hey,Wrire a code in python for adding two numbers
A:def add(a,b):
  return a+b
"""
response=client.chat.completions.create(
  model="gemini-3.1-flash-lite",
  messages=[
    {"role":"user","content":question},
    {"role":"system","content":SYSTEM_PROMPT}
    ]
)

print(response.choices[0].message.content)