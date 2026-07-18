from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(
  api_key=os.getenv("api_key"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
question=input("Enter your question:")
#Zero shot prompting
SYSTEM_PROMPT="Your job is to only answer coding related problems do not answer anything else your name is gubbinlubbin you are a bot for a code helper company" \
"If user asks anything else just say sorry and tell about yourself who are you why are you "
response=client.chat.completions.create(
  model="gemini-3.1-flash-lite",
  messages=[
    {"role":"user","content":question},
    {"role":"system","content":SYSTEM_PROMPT}
    ]
)

print(response.choices[0].message.content)